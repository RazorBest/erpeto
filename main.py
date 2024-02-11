from __future__ import annotations
import base64
import json
import random
import re
import string
import sys
import time
import urllib

from enum import Enum
from typing import AsyncIterator, Any, Callable, cast, Iterator, Optional, Protocol, Sequence, TypeVar, Union, TYPE_CHECKING

import dateutil.parser
import pycdp
import requests
import twisted.internet.reactor

from bs4 import BeautifulSoup
from twisted.python.log import err
from twisted.internet import defer, threads
from twisted.internet.interfaces import IReactorCore
from pycdp import cdp
from pycdp.browser import ChromeLauncher
from pycdp.twisted import connect_cdp

from cdprecorder import filters, generate_python
from cdprecorder.action import (
    BrowserAction,
    InputAction,
    HttpAction,
    LowercaseStr,
    RequestAction,
    ResponseAction,
    response_action_from_python_response,
)
from cdprecorder.http_types import (
    Cookie,
    parse_cookie
)
from cdprecorder.datasource import (
    DataSource,
    IntermediaryDataSource,
    SubstrSource,
    StrSource,
    HeaderSource,
    CookieSource,
    BodySource,
    JSONSource,
)
from cdprecorder.datatarget import (
    CookieTarget,
    HeaderTarget,
    BodyTarget,
)
from cdprecorder.str_evaluator import randomness_score

if TYPE_CHECKING:
    import builtins
    import http

    import bs4

    from pycdp.cdp.util import T_JSON_DICT
    from twisted.python.failure import Failure

    class CdpEvent(Protocol):
        def to_json(self) -> T_JSON_DICT: ...

    class HttpTarget(Protocol):
        def apply(self, action: HttpAction, prev_actions: list[Optional[HttpAction]]) -> None: ...

    RequestInfo = Union[
        #cdp.network.RequestWillBeSent,
        cdp.network.Request,
        cdp.network.RequestWillBeSentExtraInfo,
        #cdp.network.ResponseReceived,
        cdp.network.Response,
        cdp.network.ResponseReceivedExtraInfo,
        "HttpAction",
        requests.models.Response
    ]


# https://github.com/twisted/twisted/issues/9909
reactor = cast(IReactorCore, twisted.internet.reactor)

CONST_HEADERS = [
    "user-agent",
    "origin",
    "referer",
    "content-length",
    "sec-ch-ua-platform",
    "sec-ch-ua-mobile",
    "sec-ch-ua",
    "content-type",
    "accept",
    "x-requested-with"
]

cdp_host = "localhost"
cdp_port = 9222

cdp_url = f"http://{cdp_host}:{cdp_port}"


def is_url_ignored(url: str, origin: Optional[str] = None) -> bool:
    # Ignore data URLs: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs
    if url.startswith("data:"):
        return True
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    if path.endswith(".js") or path.endswith(".svg") or path.endswith(".css"):
        return True

    if origin and not url_belongs_to_origin(origin, url):
        return True

    return False


def extract_origin(url: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def url_belongs_to_origin(origin: str, url: str) -> bool:
    url_origin = extract_origin(url)
    return url_origin == origin


def randomstr(length: int) -> str:
    return "".join(random.choices(string.printable, k=length))
        

class HttpCommunication:
    """Represents a collection of network CDP events with the same request id.
    """
    def __init__(self,
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


def search_str_in_soup(soup: BeautifulSoup, text: str) -> Union[bs4.element.Tag, bs4.element.NavigableString, None]:
    def tag_contains_str(tag: bs4.Tag) -> bool:
        for key, val in tag.attrs.items():
            # Multi-valued attrs: https://beautiful-soup-4.readthedocs.io/en/latest/#multi-valued-attributes
            if isinstance(val, list): # type: ignore[unreachable]
                for elem in val: # type: ignore[unreachable]
                    if text in elem:
                        return True

            if text in val:
                return True

        if tag.string is not None and text in tag.string:
            return True

        return False

    return soup.find(tag_contains_str)


def get_selector_from_tag(tag: bs4.Tag) -> str:
    # TODO: implement
    return ""
    

def find_context_html(data: str, text: str):
    soup = BeautifulSoup(data)   
    tag = search_str_in_soup(soup, text)
    # TODO: return something


def find_context_bytes(data: bytes, text_to_find: bytes) -> Optional[bytes]:
    start = data.find(text_to_find)
    if start == -1:
        return None

    end = start + len(text_to_find)
    if len(data) < 50 or start < 6:
        if end - start == len(data):
            return b".*"

        return b"(?:.{" + str(start).encode() + b"}).{" + str(end - start).encode() + b"}"
    
    offset = 6
    while start >= offset:
        prefix = re.escape(data[start-offset:start])
        suffix = re.escape(data[end:end+offset])
        pattern = b"(?:" + prefix + b").{" + str(end - start).encode() + b"}(?:" + suffix + b")"
        matches = re.findall(pattern, data)
        if len(matches) == 0:
            raise Exception
        if len(matches) == 1:
            break

        offset += 6

    return pattern

def find_context_str(data: str, text: str) -> Optional[str]:
    start = data.find(text)
    if start == -1:
        return None

    end = start + len(text)
    if len(data) < 50 or start < 6:
        if end - start == len(data):
            return ".*"

        return "(?:.{" + str(start) + "}).{" + str(end - start) + "}"
    
    prefix = re.escape(data[start-6:start])
    suffix = re.escape(data[end:end+6])
    return "(?:" + prefix + ").{" + str(end - start) + "}(?:" + suffix + ")"


T = TypeVar("T", str, bytes)
def find_context(data: T, text: T, data_type: str = "str") -> Optional[T]:
    if data_type == "str":
        if not isinstance(data, str):
            raise Exception
        return find_context_str(data, text)
    if data_type == "bytes":
        if not isinstance(data, bytes):
            raise Exception
        return find_context_bytes(data, text)
    if data_type == "html":
        if not isinstance(data, str):
            raise Exception
        return find_context_html(data, text)

    return None
    

def look_for_str_in_response(index: int, text: str, action: ResponseAction) -> Optional[DataSource]:
    text_bin = text.encode()

    if action.body and action.body.find(text_bin) != -1:
        context = find_context(action.body, text_bin, data_type="bytes")
        # TODO: do something with the context

    for key, value in action.headers.items():
        escaped_value = value
        if key.lower() == "set-cookie":
            escaped_value = urllib.parse.unquote(value)

        if text in escaped_value:
            if key.lower() == "set-cookie":
                values = value.split("\n")
                cookies = [parse_cookie(val) for val in values]
                for cookie in cookies:
                    if text in cookie.value:
                        start = cookie.value.find(text)
                        end = start + len(text)
                        if end - start == len(cookie.value):
                            strcontext = ".*"
                        else:
                            strcontext = "(?:.{" + str(start) + "}).{" + str(end - start) + "}"

                        # match = re.match(strcontext, cookie.value)

                        source = CookieSource(index, cookie.name, strcontext)
                        break
                else:
                    # TODO: treat this case
                    pass

                return source


            else:
                pass
                """
                start = escaped_value.find(text)
                end = start + len(text)
                if end - start == len(escaped_value):
                    strcontext = ".*"
                else:
                    strcontext = "(?:.{" + str(start) + "}).{" + str(end - start) + "}"
                source = HeaderSource(index, key.lower(), strcontext)

                return source
                """
    return None


def look_for_str_in_input_action(index: int, text: str, action: InputAction) -> Optional[DataSource]:
    if action.value in text:
        start = text.find[action.value]
        end = start + len(action.value)

        src1 = InputSource(action.value)
        src2 = SubstrSource(src1, start, end)

        return src2

    return None
    

def look_for_str_in_actions(text: str, actions: list[HttpAction]) -> Union[tuple[None, None], tuple[int, DataSource]]:
    """Takes a string and looks for it through the actions present in the actions."""
    for index, action in enumerate(actions):
        source = None
        if isinstance(action, ResponseAction):
            source = look_for_str_in_response(index, text, action)
        elif isinstance(actions, InputAction):
            source = look_for_str_in_input_action(index, text, action)

        if source is not None:
            return index, source
            


    return None, None


def analyze_actions(actions: list[BrowserAction]) -> None:
    for i, action in enumerate(actions):
        if isinstance(action, RequestAction):
            for key, value in action.headers.items():
                if key.lower() in CONST_HEADERS:
                    continue
                score = randomness_score(value)
                if score > 50:
                    index, source = look_for_str_in_actions(value, actions[:i])
                    if source:
                        target: HttpTarget = HeaderTarget(source, key, value)
                        action.targets.append(target)

                        print(f"Found {source.__class__.__name__} for {target.__class__.__name__}")

            for cookie in action.cookies:
                if not cookie.value:
                    continue
                score = randomness_score(cookie.value)
                if score > 50:
                    index, source = look_for_str_in_actions(cookie.value, actions[:i])
                    if source:
                        target = CookieTarget(cookie.name, source)
                        action.targets.append(target)

                        print(f"Found {source.__class__.__name__} for {target.__class__.__name__}")

            if action.body:
                body_bytes = action.body
                try:
                    body = body_bytes.decode("utf8")
                    json.loads(body)
                    source_group = JSONSource(body)
                    has_sources = False
                    for field in source_group.targets:
                        index, source = look_for_str_in_actions(field.value, actions[:i])
                        if source:
                            has_sources = True
                            field.source = source

                    if has_sources:
                        action.targets.append(BodyTarget(source_group))
                        print(f"Found {source_group.__class__.__name__} for BodyTarget")
                except json.JSONDecodeError:
                    # This shouldn't be functional
                    score = randomness_score(body)
                    if score > 50:
                        index, source = look_for_str_in_actions(body, actions[:i])
                        if source:
                            target = BodyTarget(source)
                            action.targets.append(target)
                            print(f"Found {source.__class__.__name__} for {target.__class__.__name__}")


def generate_action(action: HttpAction, prev_new_actions: list[Optional[HttpAction]]) -> RequestAction:
    new_action = RequestAction()
    new_action.shallow_copy_from_action(action)
    for target in action.targets:
        target.apply(new_action, prev_new_actions)

    return new_action
    

def run_actions(actions: list[HttpAction]) -> None:
    new_actions: list[Optional[HttpAction]] = []

    for action in actions:
        if isinstance(action, RequestAction):
            new_action = generate_action(action, new_actions)
            new_actions.append(new_action)

            with requests.Session() as session:
                req = requests.Request(
                    method=new_action.method,
                    url=new_action.url,
                    headers=new_action.headers,
                    data=new_action.body,
                    cookies=new_action.cookies_to_dict(),
                )
                prepared_request = req.prepare()
                resp = session.send(prepared_request, allow_redirects=False)
                resp_action = response_action_from_python_response(resp)
                new_actions.append(resp_action)

                print(f"{new_action.method} {new_action.url} - {resp.status_code}")

        elif not isinstance(action, ResponseAction):
            new_actions.append(None)


def to_cdp_event(event: CdpEvent) -> dict[str, Union[str, T_JSON_DICT]]:
    cdp_method = None
    for key, val in cdp.util._event_parsers.items():
        if val == event.__class__:
            cdp_method = key
            break
    else:
        raise Exception

    return {
        "method": cdp_method,
        "params": event.to_json(),
        "type": "recv",
        "domain": "-",
    }


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
    communications = []
    request_map = {}

    start_time = time.time()
    async for evt in listener:
        if time.time() - start_time > timeout:
            break

        if isinstance(evt, cdp.network.RequestWillBeSent) or \
                isinstance(evt, cdp.network.RequestWillBeSentExtraInfo) or \
                isinstance(evt, cdp.network.ResponseReceived) or \
                isinstance(evt, cdp.network.ResponseReceivedExtraInfo):
            if evt.request_id not in request_map:
                comm = HttpCommunication(evt.request_id)
                communications.append(comm)
                request_map[evt.request_id] = comm

        if isinstance(evt, cdp.runtime.ConsoleAPICalled):
            if evt.type_ != 'log' or \
                (isinstance(evt.args[0].value, str) and not evt.args[0].value.startswith(keystr)):
                continue

            printed_arg = evt.args[0]
            if printed_arg.value:
                value = printed_arg.value.removeprefix(keystr)
                data = json.loads(value) 
            else:
                if evt.args[0].object_id is not None:
                    result = await target_session.execute(cdp.runtime.get_properties(evt.args[0].object_id, own_properties=True))
                    data = {attr.name: attr.value.value for attr in result[0]}

            if data["event"] == "input":
                action = InputAction(data["value"], data["selector"], data["timestamp"])
                communications.append(action)

        elif isinstance(evt, cdp.network.RequestWillBeSent):
            cdp_req = evt.request
            request_id = evt.request_id

            request_map[request_id].add_event(evt)

            if not collect_all and \
                    (is_url_ignored(cdp_req.url, start_origin) or urlfilter.should_block(evt.request.url)):
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

            except pycdp.exceptions.CDPBrowserError as exc:
                print("  --cdp-browser-error")

            request_map[request_id].add_event(evt)
            request_map[request_id].response_bodies.append(body)

    return communications


def get_only_http_actions(actions: list[BrowserActions]) -> list[HttpActions]:
    return [action for action in actions if isinstance(action, HttpAction)]

def _generate_events_with_redirects_extracted(events: list[CdpEvent]) -> list[CdpEvent]:
    new_events = []
    future_events: list[CdpEvents] = []
    wait_response_extra = False
    wait_request_extra = False
    wait_extra = False
    for evt in events:
        if wait_extra:
            if isinstance(evt, cdp.network.RequestWillBeSentExtraInfo) and not wait_request_extra \
                    or isinstance(evt, cdp.network.ResponseReceivedExtraInfo) and not wait_response_extra:
                wait_extra = False 
                new_events += future_events
                future_events = []

            if isinstance(evt, cdp.network.RequestWillBeSentExtraInfo):
                wait_request_extra = False
            elif isinstance(evt, cdp.network.ResponseReceivedExtraInfo):
                wait_response_extra = False
            wait_extra = wait_response_extra or wait_request_extra

            new_events.append(evt)
            continue
        else:
            new_events += future_events
            future_events = []

        future_events.append(evt)
        if not isinstance(evt, cdp.network.RequestWillBeSent):
            continue

        if not evt.redirect_response:
            new_events += future_events
            future_events = []
            wait_extra = False
        else:
            if evt.redirect_has_extra_info:
                wait_response_extra = True
                wait_request_extra = True
                wait_extra = True

            response_evt = cdp.network.ResponseReceived(
                request_id=evt.request_id,
                loader_id=evt.loader_id,
                timestamp=evt.timestamp,
                type_=evt.type_,
                response=evt.redirect_response,
                has_extra_info=evt.redirect_has_extra_info,
                frame_id=evt.frame_id,
            )
            new_events.append(response_evt)

    new_events += future_events

    return new_events
    

def parse_communications_into_actions(communications: list[Union[HttpCommunication, InputActioni]]) -> list[BrowserAction]:
    actions: list[BrowserAction] = []

    for comm in communications:
        if not isinstance(comm, HttpCommunication):
            actions.append(comm)
            continue

        if comm.ignored:
            continue

        response_bodies = list(comm.response_bodies)

        curr_request: Optional[RequestAction] = None
        request_extra: Optional[RequestAction] = None
        curr_response: Optional[ResponseAction] = None
        response_extra: Optional[ResponseAction] = None
        events = _generate_events_with_redirects_extracted(comm.events)
        print("--------------------------------------------------------")
        for evt in events:
            info_str = f"{evt.__class__.__name__} "
            #info_str += str(getattr(evt, "headers", getattr(getattr(evt, "request", None), "headers", None))))
            info_str += str(getattr(evt, "method", getattr(getattr(evt, "request", None), "method", None)))
            
            print(info_str)
            if isinstance(evt, cdp.network.RequestWillBeSent):
                if curr_request is not None:
                    if all((curr_request, request_extra, curr_response)):
                        curr_request.has_response = True
                        actions.append(curr_request)
                        actions.append(curr_response)
                    else:
                        actions.append(curr_request)
                        if curr_response is not None:
                            curr_request.has_response = True
                            actions.append(curr_response)

                    curr_request = None
                    request_extra = None
                    curr_response = None

                """
                if curr_request is not None:
                    # Consume the previous request
                    if curr_response:
                        curr_request.has_response = True
                    actions.append(curr_request)
                    curr_request = None
                    request_extra = None

                    if curr_response:
                        # Consume the previous response
                        actions.append(curr_response)
                    if response_extra:
                        raise Exception
                    curr_response = None
                """

                curr_request = RequestAction()
                curr_request.update_info(evt.request)
                if evt.request.has_post_data and evt.request.post_data:
                    # TODO: Check if bytes in other entry
                    curr_request.set_body(evt.request.post_data.encode())

                if request_extra is not None:
                    curr_request.merge(request_extra)

            elif isinstance(evt, cdp.network.RequestWillBeSentExtraInfo):
                if request_extra is not None:
                    if all((curr_request, request_extra, curr_response)):
                        curr_request.has_response = True
                        actions.append(curr_request)
                        curr_request = None
                        request_extra = None

                        actions.append(curr_response)
                        curr_response = None

                """
                if curr_request is not None and request_extra is not None:
                    # Consume the previous request
                    if curr_response:
                        curr_request.has_response = True
                    actions.append(curr_request)
                    curr_request = None
                    request_extra = None

                if curr_response:
                    # Consume the previous response
                    actions.append(curr_response)
                if response_extra:
                    raise Exception
                curr_response = None
                """

                if request_extra is not None:
                    raise Exception
                request_extra = RequestAction()
                request_extra.update_info(evt)

                if curr_request is not None:
                    curr_request.merge(request_extra)
                    # request_extra = None

            elif isinstance(evt, cdp.network.ResponseReceived):
                if curr_response is None:
                    curr_response = ResponseAction(evt.response)
                else:
                    raise Exception

                if response_extra is not None:
                    # Always merge response_extra over curr_response, not the other way
                    curr_response.merge(response_extra)
                    response_extra = None

            elif isinstance(evt, cdp.network.ResponseReceivedExtraInfo):
                if curr_response is not None:
                    # Always merge response_extra over curr_response, not the other way
                    curr_response.merge(ResponseAction(evt))
                elif response_extra is None:
                    response_extra = ResponseAction(evt)
                else:
                    raise Exception

            elif isinstance(evt, cdp.network.LoadingFinished):
                # Manually inserted
                response_body = response_bodies.pop(0)
                if response_body is not None:
                    if curr_response:
                        curr_response.set_body(response_body)
                    elif response_extra:
                        response_extra.set_body(response_body)
                    else:
                        raise Exception

                if curr_request is not None:
                    if curr_response or response_extra:
                        curr_request.has_response = True
                    actions.append(curr_request)
                    curr_request = None
                if curr_response is not None:
                    actions.append(curr_response)
                    curr_response = None
                elif response_extra is not None:
                    actions.append(response_extra)
                    response_extra = None


        if curr_request is not None:
            if curr_response is not None:
                curr_request.has_response = True
            curr_request.merge(request_extra)
            actions.append(curr_request)
        if curr_response is not None:
            # Always merge response_extra over curr_response, not the other way
            curr_response.merge(response_extra)
            actions.append(curr_response)

    return actions


async def insert_js_action_listener(target_session: pycdp.twisted.CDPSession, keystr: str) -> None:
    expression = """
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

    """ + f"var _keystr01238 = {json.dumps(keystr)};"

    ret = await target_session.execute(cdp.runtime.evaluate(expression))


async def main() -> None:
    """
    chrome = ChromeLauncher(
        binary='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', # windows path
        args=['--remote-debugging-port=9222', '--incognito']
    )
    await threads.deferToThread(chrome.launch)
    """
    urlfilter = filters.URLFilter()
    """
    with open("urlfilter", "rb") as f:
        import pickle
        urlfilter = pickle.load(f)
        """

    conn = await connect_cdp(cdp_url, reactor)
    target_id = await conn.execute(cdp.target.create_target("about:blank"))
    print(target_id)
    target_session = await conn.connect_session(target_id)
    print(target_session)
    await target_session.execute(cdp.page.enable())

    await target_session.execute(cdp.network.enable())
    listener = target_session.listen(
        cdp.runtime.ConsoleAPICalled,
        cdp.network.RequestWillBeSent,
        cdp.network.RequestWillBeSentExtraInfo,
        cdp.network.ResponseReceived,
        cdp.network.ResponseReceivedExtraInfo,
        cdp.network.LoadingFinished,
        buffer_size=512,
    )

    # start_url = "https://www.google.com/intl/ro/gmail/about/"
    # start_url = "http://youtube.com/"
    await target_session.execute(cdp.page.navigate(start_url))

    # DOC: https://developer.chrome.com/docs/devtools/console/utilities
    await target_session.execute(cdp.runtime.enable())

    keystr = randomstr(32)
    await insert_js_action_listener(target_session, keystr)

    start_origin = extract_origin(start_url)
    communications = await collect_communications(target_session, listener, urlfilter, keystr, 20, False, start_origin)

    actions = parse_communications_into_actions(communications)

    analyze_actions(actions)
    #actions = get_only_http_actions(actions)
    #run_actions(actions)

    generate_python.write_python_code(actions, "generated.py")

    """
    async with target_session.wait_for(cdp.runtime.ConsoleAPICalled) as evt:
        print(evt)
        if evt.args[0].value == "click":
            for obj in evt.args:
                if obj.class_name == "PointerEvent":

                    result = await target_session.execute(cdp.runtime.get_properties(obj.object_id))
                    pointer_evt_props = result[0]
                    break
        
    for prop in pointer_evt_props:
        if prop.name == "srcElement":
            print(prop)
            result = await target_session.execute(cdp.dom.describe_node(object_id=prop.value.object_id))
            print(result)
    """


    await conn.close()
    """
    await threads.deferToThread(chrome.kill)
    """

def main_error(failure: Failure) -> None:
    err(failure) # type: ignore[no-untyped-call]
    reactor.stop()


if __name__ == "__main__":
    d = defer.ensureDeferred(main())
    d.addErrback(main_error)
    d.addCallback(lambda *args: reactor.stop())
    reactor.run()
