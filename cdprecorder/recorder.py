from __future__ import annotations

import base64
import json
import platform
import random
import string
import time
import urllib
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    AsyncIterable,
    AsyncIterator,
    Coroutine,
    Generic,
    Optional,
    TypeVar,
    Union,
    cast,
)

import pycdp
import twisted.internet.reactor
from pycdp import cdp
from pycdp.browser import ChromeLauncher
from pycdp.twisted import CDPConnection as _PyCDPConnection
from twisted.internet import defer, threads
from twisted.internet.error import ConnectionRefusedError
from twisted.internet.interfaces import IReactorCore, IReactorTime
from twisted.web.client import Agent

from . import filters
from .action import InputAction

if TYPE_CHECKING:
    import builtins

    from .type_checking import CdpEvent


class Reactor(IReactorCore, IReactorTime):  # pylint disable=too-many-ancestors
    pass


# https://github.com/twisted/twisted/issues/9909
reactor = cast(Reactor, twisted.internet.reactor)


LOGO_PATH = "./logo.png"
RECORDER_WIDGET_PATH = "./recorder_widget.js"


class AwaitableIsNotCoroutine(Exception):
    pass


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

    await target_session.execute(cdp.runtime.evaluate(expression))


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


T = TypeVar("T")


class AsyncIteratorWithTimeout(Generic[T]):
    def __init__(self, iterator: AsyncIterator[T], timeout: float, start_time: Optional[float] = None):
        self.iterator = iterator
        self.timeout = timeout
        if start_time is None:
            self.start_time = time.time()
        else:
            self.start_time = start_time

    async def __anext__(self) -> T:
        curr_time = time.time()
        remained = self.timeout - (curr_time - self.start_time)
        if remained <= 0:
            raise StopAsyncIteration

        coro = self.iterator.__anext__()
        if not isinstance(coro, Coroutine):
            raise AwaitableIsNotCoroutine
        d: defer.Deferred[T] = defer.Deferred.fromCoroutine(coro)
        d.addTimeout(remained, reactor)
        return await d

    def __aiter__(self) -> AsyncIteratorWithTimeout:
        return self


class AsyncIterableWithTimeout(Generic[T]):
    def __init__(self, iterable: AsyncIterable[T], timeout: float, start_time: Optional[float] = None):
        self.iterable = iterable
        self.timeout = timeout
        if start_time is None:
            self.start_time = time.time()
        else:
            self.start_time = start_time

    def __aiter__(self) -> AsyncIterator[T]:
        return AsyncIteratorWithTimeout(self.iterable.__aiter__(), self.timeout, self.start_time)


async def collect_communications(
    target_session: pycdp.twisted.CDPSession,
    listener: AsyncIterator[builtins.object],
    urlfilter: filters.URLFilter,
    keystr: str,
    timeout: int = 120,
    collect_all: bool = False,
    start_origin: Optional[str] = None,
) -> list[Union[HttpCommunication, InputAction]]:
    """Takes a cdp session, listens for events, and generates a list of
    communications.

    Might also send CDP messages to get additional info about JavaScript
    objects or HTTP body.

    Args:
        target_session: The CDP session.
        listener: An async iterator that generates CDP events.
        urlfilter: Tells which URLs to ignore.
        keystr: A unique string used to distinguish console log messages.
        timeout: When to stop listening.

    Returns:
        A list of communications.
    """
    communications: list[Union[HttpCommunication, InputAction]] = []
    request_map = {}

    timed_listener = AsyncIterableWithTimeout(listener, timeout)
    async for evt in timed_listener:
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


class CDPConnection(_PyCDPConnection):
    # Remove `retry_on` wrapper from function
    connect = _PyCDPConnection.connect.__wrapped__  # type: ignore[attr-defined] # pylint: disable=no-member


# Default path: Windows
CHROME_BINARY = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
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
    fail_if_no_connection: bool = False

    @property
    def cdp_url(self) -> str:
        return f"http://{self.cdp_host}:{self.cdp_port}"


async def obtain_active_tab(
    targets: list[cdp.target.TargetInfo], conn: CDPConnection
) -> Optional[cdp.target.TargetInfo]:
    if not targets:
        return None

    visible_targets = []
    for target in targets:
        session = await conn.connect_session(target.target_id)
        await session.execute(cdp.runtime.enable())
        ret, _ = await session.execute(cdp.runtime.evaluate("document.hidden"))
        print(ret)
        if not ret.type_ == "boolean" or ret.value is not True:
            visible_targets.append(target)
        ret, _ = await session.execute(cdp.runtime.evaluate("browser.tabs"))
        print(ret)

    if len(visible_targets) == 1:
        return visible_targets[0]

    return None


async def obtain_cdp_target_id(conn: CDPConnection) -> cdp.target.TargetID:
    targets = await conn.execute(cdp.target.get_targets())
    page_targets = []
    for target in targets:
        if target.type_ == "page" and not target.url.startswith("devtools://"):
            page_targets.append(target)

    desired_target = None
    if len(page_targets) == 1:
        desired_target = page_targets[0]
    elif len(page_targets) > 0:
        desired_target = await obtain_active_tab(page_targets, conn)

    if desired_target:
        return desired_target.target_id

    context_id = None
    context_id = await conn.execute(cdp.target.create_browser_context())
    target_id = await conn.execute(cdp.target.create_target("about:blank", browser_context_id=context_id))

    return target_id


class RuntimeContext:
    def __init__(
        self, target_session: pycdp.twisted.CDPSession, context_name: str, context_id: cdp.runtime.ExecutionContextId
    ):
        self.target_session = target_session
        self.context_name = context_name
        self.context_id = context_id
        self.start_time: Optional[float] = None

    async def start_timer(self) -> None:
        await self.target_session.execute(cdp.runtime.evaluate("startTimerIfElemLoaded()", context_id=self.context_id))
        self.start_time = time.time()

    async def _send_state_elapsed(self, start_time: float) -> None:
        elapsed = time.time() - start_time
        await self.target_session.execute(
            cdp.runtime.evaluate(f"setTimerElapsed({elapsed})", context_id=self.context_id)
        )

    async def send_state(self) -> None:
        if self.start_time is not None:
            await self._send_state_elapsed(self.start_time)


async def insert_widget_extension(target_session: pycdp.twisted.CDPSession) -> RuntimeContext:
    from importlib import resources as impresources

    logo_file = impresources.files(__package__) / LOGO_PATH
    widget_file = impresources.files(__package__) / RECORDER_WIDGET_PATH

    data_url = ""
    with logo_file.open("rb") as file:
        data = file.read()
        encoded = base64.b64encode(data).decode("utf-8")
        extension = LOGO_PATH.rsplit(".", maxsplit=1)[-1]
        data_url = f"data:image/{extension};base64,{encoded}"

    expression = f"""const logo_src = "{data_url}";\n"""

    with widget_file.open("r", encoding="utf8") as file:
        expression += file.read()

    runtime_init_timeout = 5
    js_context_id = None
    recorder_context_name = "recorder_window_" + randomstr(16)

    await target_session.execute(cdp.page.runtime.enable())

    try:
        runtime_listener = target_session.listen(cdp.runtime.ExecutionContextCreated)
        await target_session.execute(
            cdp.page.add_script_to_evaluate_on_new_document(
                expression, run_immediately=True, world_name=recorder_context_name
            )
        )
        timed_runtime_listener = AsyncIterableWithTimeout(runtime_listener, runtime_init_timeout)
        async for evt in timed_runtime_listener:
            if evt.context.name == recorder_context_name:
                js_context_id = evt.context.id_
                break
    except defer.TimeoutError as exc:
        raise Exception from exc
    finally:
        target_session.close_listeners()

    if js_context_id is None:
        raise Exception

    runtime = RuntimeContext(target_session, recorder_context_name, js_context_id)
    await runtime.start_timer()
    await runtime.send_state()

    return runtime


async def record(options: RecorderOptions) -> list[Union[HttpCommunication, InputAction]]:
    urlfilter = filters.URLFilter()

    try:
        conn = CDPConnection(options.cdp_url, Agent(reactor), reactor)  # type: ignore[no-untyped-call]
        await conn.connect()
    except ConnectionRefusedError:
        if options.fail_if_no_connection:
            raise ConnectionRefusedError
        chrome = ChromeLauncher(binary=options.binary, args=["--remote-debugging-port=9222", "--incognito"])
        await threads.deferToThread(chrome.launch)  # type: ignore[no-untyped-call]
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

    if options.start_url:
        print(f"info: {options.start_url!r}")
        start_url = options.start_url
        await target_session.execute(cdp.page.navigate(start_url))
    else:
        info = await target_session.execute(cdp.target.get_target_info())
        # The path of this can be set with the History API
        # But the origin can't be changed
        start_url = info.url

    runtime = await insert_widget_extension(target_session)

    runtime_listener = target_session.listen(cdp.runtime.ExecutionContextCreated)

    runtime_init_timeout = 15
    timed_runtime_listener = AsyncIterableWithTimeout(runtime_listener, runtime_init_timeout)
    try:
        async for evt in timed_runtime_listener:
            if evt.context.name == runtime.context_name:
                js_context_id = evt.context.id_
                runtime.context_id = js_context_id
                await runtime.send_state()
    except defer.TimeoutError as exc:
        raise Exception from exc

    keystr = randomstr(32)
    await insert_js_action_listener(target_session, keystr)

    start_origin = None
    if options.keep_only_same_origin_urls:
        start_origin = extract_origin(start_url)

    communications = await collect_communications(target_session, listener, urlfilter, keystr, 20, False, start_origin)

    await conn.close()

    return communications
