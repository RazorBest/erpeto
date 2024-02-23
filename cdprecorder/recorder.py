from __future__ import annotations

import asyncio
import base64
import json
import random
import platform
import string
import time
import urllib
from dataclasses import dataclass
from typing import TYPE_CHECKING, AsyncIterator, Optional, Union, cast

import pycdp
import twisted.internet.reactor
from pycdp import cdp
from pycdp.browser import ChromeLauncher
from pycdp.twisted import CDPConnection as _PyCDPConnection
from twisted.internet import threads, defer
from twisted.internet.interfaces import IReactorCore
from twisted.internet.error import ConnectionRefusedError
from twisted.web.client import Agent

from . import filters
from .action import InputAction

if TYPE_CHECKING:
    import builtins

    from .type_checking import CdpEvent

# https://github.com/twisted/twisted/issues/9909
reactor = cast(IReactorCore, twisted.internet.reactor)


def randomstr(length: int) -> str:
    return "".join(random.choices(string.printable, k=length))


def extract_origin(url: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def url_belongs_to_origin(url: str, origin: str) -> bool:
    return extract_origin(url) == extract_origin(origin)


def is_url_ignored(url: str, origin: Optional[str] = None) -> bool:
    # Ignore data URLs: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs
    if url.startswith("data:"):
        return True
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    if path.endswith(".js") or path.endswith(".svg") or path.endswith(".css"):
        return True

    if origin and not url_belongs_to_origin(url, origin):
        return True

    return False


async def insert_js_action_listener(target_session: pycdp.twisted.CDPSession, keystr: str) -> None:
    expression = (
        """
    get_element_selector = (target) => {
        const tag_selector = target.tagName.toLowerCase();
        const classes = target.className.split(' ');
        let cls_selector = '';
        classes.forEach(cls => {
            if (cls.trim().length == 0) {
                return;
            }
            cls_selector += '.' + cls;
        })
        const id_selector = event.id ? ('#' + event.id) : '';

        let attr_selector = '';
        for (let i = 0; i < target.attributes.length; i++) {
            const attr = target.attributes.item(i)
            if (attr.name == 'id' || attr.name == 'class') {
                continue
            }
            attr_selector += '[' + attr.name + '="' + attr.value + '"]';
        }

        let index_selector = '';
        if (target.parentNode.children.length > 1) {
            const index = Array.from(target.parentNode.children).indexOf(target) + 1;
            index_selector = ":nth-child(" + index.toString() + ")";
        }
        // Should count last of type

        selector = tag_selector + id_selector + cls_selector + attr_selector + index_selector;

        return selector;
    }
    getSelectorToRoot = (target) => {
        let selector = "";

        selector += get_element_selector(target);
        target = target.parentNode;
        while (target) {
            if (!target.tagName) {
                if (!target.host) {
                    break
                }
                // If shadow root
                target = target.host;
            }
            selector = get_element_selector(target) + '>' + selector;
            target = target.parentNode;
        }

        return selector;
    }
    addEventListener('click', (event) => {
        // Try to get the original target, even if in shadow DOM
        const timestamp = event.timeStamp;
        const target = event.composedPath()[0];
        const selector = getSelectorToRoot(target);

        console.log(_keystr01238 + JSON.stringify({"event": "click", timestamp, selector}))
    });

    addEventListener('keypress', (event) => {
        const charCode = event.charCode;
        const timestamp = event.timeStamp;
        const target = event.composedPath()[0];
        const selector = getSelectorToRoot(target);
        const value = target.value;

        console.log(_keystr01238 + JSON.stringify({"event": "keypress", timestamp, selector, value, charCode}));
    });

    addEventListener('input', (event) => {
        const target = event.composedPath()[0];
        const selector = getSelectorToRoot(target);
        const value = target.value;
        const timestamp = event.timeStamp;

        console.log(_keystr01238 + JSON.stringify({"event": "input", timestamp, selector, value}));
    });

    """
        + f"var _keystr01238 = {json.dumps(keystr)};"
    )

    ret = await target_session.execute(cdp.runtime.evaluate(expression))


class HttpCommunication:
    """Represents a collection of network CDP events with the same request id."""

    def __init__(
        self,
        request_id: cdp.network.RequestId,
        ignored: bool = False,
        events: Optional[list[CdpEvent]] = None,
        response_bodies: Optional[list[Optional[bytes]]] = None,
    ):
        self.request_id = request_id
        self.ignored = ignored
        self.events = events if events is not None else []
        self.response_bodies: list[Optional[bytes]] = []
        if response_bodies:
            self.response_bodies = response_bodies

    def add_event(self, event: CdpEvent) -> None:
        self.events.append(event)

    def __str__(self) -> str:
        name = self.__class__.__name__
        text = f"{name}(reuquest_id={self.request_id}, ignored={self.ignored})"

        for event in self.events:
            text += "\n" + str(event)

        return text

    def __eq__(self, obj: object) -> bool:
        if type(self) != type(obj):
            return False
        for key, val in vars(self).items():
            if not hasattr(obj, key):
                return False
            if val != getattr(obj, key):
                return False

        return True


class AsyncIteratorWithTimeout:
    def __init__(self, aiter: AsyncIterable, timeout: float, start_time: Optional[float] = None):
        self.aiter = aiter
        self.timeout = timeout
        if start_time is None:
            self.start_time = time.time()
        else:
            self.start_time = start_time

        self.timeout_waiter = None

    async def wait_for_next(self, coro):
        result = await coro
        if self.timeout_waiter:
            self.timeout_waiter.cancel()
            self.timeout_waiter = None

        return result

    async def __anext__(self):
        curr_time = time.time()
        remained = self.timeout - (curr_time - self.start_time)
        if remained <= 0:
            raise StopAsyncIteration

        d = defer.Deferred.fromCoroutine(self.aiter.__anext__())
        d.addTimeout(remained, reactor)
        #self.timeout_waiter = reactor.callLater(int(remained), lambda : d.cancel())
        return await d


class AsyncIterableWithTimeout:
    def __init__(self, iterator: AsyncIterable, timeout: float, start_time: Optional[float] = None):
        self.iterator = iterator
        self.timeout = timeout
        if start_time is None:
            self.start_time = time.time()
        else:
            self.start_time = start_time

    def __aiter__(self):
        return AsyncIteratorWithTimeout(self.iterator.__aiter__(), self.timeout, self.start_time)



async def collect_communications(
    target_session: pycdp.twisted.CDPSession,
    listener: AsyncIterator[builtins.object],
    urlfilter: filters.URLFilter,
    keystr: str,
    timeout: int = 8,
    collect_all: bool = False,
    start_origin: Optional[str] = None,
) -> list[Union[HttpCommunication, InputAction]]:
    """Takes a cdp session, listens for events, and generates a list of
    communications.

    Might also send CDP messages to get additional info about JavaScript
    objects or HTTP body.

    Args:
        target_session: The CDP session.
        listener: An asyncio iterator that generates CDP events.
        urlfilter: Tells which URLs to ignore.
        keystr: A unique string used to distinguish console log messages.
        timeout: When to stop listening.

    Returns:
        A list of communications.
    """
    communications: list[Union[HttpCommunication, InputAction]] = []
    request_map = {}

    start_time = time.time()
    listener = AsyncIteratorWithTimeout(listener, 60)
    async for evt in listener:
        """
        if time.time() - start_time > timeout:
            break
        """

        if isinstance(
            evt,
            (
                cdp.network.RequestWillBeSent,
                cdp.network.RequestWillBeSentExtraInfo,
                cdp.network.ResponseReceived,
                cdp.network.ResponseReceivedExtraInfo,
            ),
        ):
            if evt.request_id not in request_map:
                comm = HttpCommunication(evt.request_id)
                communications.append(comm)
                request_map[evt.request_id] = comm

        if isinstance(evt, cdp.runtime.ConsoleAPICalled):
            if evt.type_ != "log" or (isinstance(evt.args[0].value, str) and not evt.args[0].value.startswith(keystr)):
                continue

            printed_arg = evt.args[0]
            if printed_arg.value:
                value = printed_arg.value.removeprefix(keystr)
                data = json.loads(value)
            else:
                if evt.args[0].object_id is not None:
                    result = await target_session.execute(
                        cdp.runtime.get_properties(evt.args[0].object_id, own_properties=True)
                    )
                    data = {attr.name: attr.value.value for attr in result[0] if attr.value}

            if data["event"] == "input":
                action = InputAction(data["value"], data["selector"], data["timestamp"])
                communications.append(action)

        elif isinstance(evt, cdp.network.RequestWillBeSent):
            cdp_req = evt.request
            request_id = evt.request_id

            request_map[request_id].add_event(evt)

            if not collect_all and (
                is_url_ignored(cdp_req.url, start_origin) or urlfilter.should_block(evt.request.url)
            ):
                request_map[request_id].ignored = True
        elif isinstance(evt, cdp.network.RequestWillBeSentExtraInfo):
            if request_map[evt.request_id].ignored:
                continue
            request_map[evt.request_id].add_event(evt)
        elif isinstance(evt, cdp.network.ResponseReceived):
            if request_map[evt.request_id].ignored:
                continue
            request_map[evt.request_id].add_event(evt)
        elif isinstance(evt, cdp.network.ResponseReceivedExtraInfo):
            if request_map[evt.request_id].ignored:
                continue
            request_map[evt.request_id].add_event(evt)
        elif isinstance(evt, cdp.network.LoadingFinished):
            request_id = evt.request_id
            if request_id not in request_map or request_map[request_id].ignored:
                continue

            body = None
            try:
                cdp_body_result = await target_session.execute(cdp.network.get_response_body(request_id))
                resulted_body, is_base_64 = cdp_body_result
                if is_base_64:
                    body = base64.b64decode(resulted_body)
                else:
                    body = resulted_body.encode()

            except pycdp.exceptions.CDPBrowserError:
                print("  --cdp-browser-error")

            request_map[request_id].add_event(evt)
            request_map[request_id].response_bodies.append(body)

    return communications


# Default path: Windows
CHROME_BINARY = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
if platform.system() == "Linux":
    CHROME_BINARY = "/usr/bin/google-chrome-stable"
if platform.system() == "Darwin":
    CHROME_BINARY = r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"


@dataclass(frozen=True)
class RecorderOptions:
    start_url: str
    keep_only_same_origin_urls: bool = True
    binary: str = CHROME_BINARY
    cdp_host: str = "localhost"
    cdp_port: int = 9222

    @property
    def cdp_url(self) -> str:
        return f"http://{self.cdp_host}:{self.cdp_port}"


async def obtain_active_tab(targets, conn: CDPConnection):
    if not targets:
        return None

    visible_targets = []
    for target in targets:
        session = await conn.connect_session(target.target_id)
        await session.execute(cdp.runtime.enable())
        ret, _ = await session.execute(cdp.runtime.evaluate("document.hidden"))
        print(ret)
        if not ret.type_ == "boolean" or ret.value != True:
            visible_targets.append(target)
        ret, _ = await session.execute(cdp.runtime.evaluate("browser.tabs"))
        print(ret)

    if len(visible_targets) == 1:
        return visible_targets[0]

    return None



async def record(options: RecorderOptions) -> list[Union[HttpCommunication, InputAction]]:
    #urlfilter = filters.URLFilter()

    try:
        conn = CDPConnection(options.cdp_url, Agent(reactor), reactor)
        await conn.connect()
    except ConnectionRefusedError:
        if options.fail_if_no_connection:
            raise ConnectionRefusedError
        chrome = ChromeLauncher(
            binary=options.binary,
            args=['--remote-debugging-port=9222', '--incognito']
        )
        await threads.deferToThread(chrome.launch)
        await conn.connect()

    target_id = await obtain_cdp_target_id(conn)
    target_session = await conn.connect_session(target_id)
    await target_session.execute(cdp.page.enable())
    await target_session.execute(cdp.page.bring_to_front())

    # Clean remaining data from possible previous run
    await target_session.execute(cdp.runtime.disable())
    await target_session.execute(cdp.runtime.enable())

    await target_session.execute(cdp.network.enable())
    listener = target_session.listen(
        cdp.runtime.ConsoleAPICalled,
        cdp.network.RequestWillBeSent,
        cdp.network.RequestWillBeSentExtraInfo,
        cdp.network.ResponseReceived,
        cdp.network.ResponseReceivedExtraInfo,
        cdp.network.LoadingFinished,
        buffer_size=1024,
    )

    start_url = options.start_url

    await target_session.execute(cdp.page.navigate(start_url))

    # DOC: https://developer.chrome.com/docs/devtools/console/utilities
    await target_session.execute(cdp.runtime.enable())

    keystr = randomstr(32)
    await insert_js_action_listener(target_session, keystr)

    start_origin = None
    if options.keep_only_same_origin_urls:
        start_origin = extract_origin(start_url)

    communications = await collect_communications(target_session, listener, urlfilter, keystr, 20, False, start_origin)

    await conn.close()

    return communications
