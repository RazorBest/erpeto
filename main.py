from __future__ import annotations
import base64
import json
import re
import sys
import urllib

from enum import Enum
from typing import AsyncIterator, Any, Callable, cast, Iterator, Optional, Protocol, Sequence, TypeVar, Union, TYPE_CHECKING

import pycdp
import requests
import twisted.internet.reactor

from bs4 import BeautifulSoup
from twisted.python.log import err
from twisted.internet import defer, threads
from twisted.internet.interfaces import IReactorCore
from pycdp import cdp

from cdprecorder import generate_python
from cdprecorder.action import (
    BrowserAction,
    InputAction,
    HttpAction,
    LowercaseStr,
    RequestAction,
    ResponseAction,
    response_action_from_python_response,
)
from cdprecorder.datasource import (
    DataSource,
    IntermediaryDataSource,
    SubstrSource,
    StrSource,
    HeaderSource,
    JSONFieldTarget,
    JSONContainer,
    CookieSource,
    BodySource,
)
from cdprecorder.datatarget import (
    CookieTarget,
    HeaderTarget,
    BodyTarget,
)
from cdprecorder.http_types import (
    Cookie,
    parse_cookie,
)
from cdprecorder.json_analyser import JSONSchema
from cdprecorder.recorder import (
    HttpCommunication,
    RecorderOptions,
    record,
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
                    schema = JSONSchema(body)
                    has_sources = False
                    json_targets = []
                    for field in schema.fields:
                        index, source = look_for_str_in_actions(field.value, actions[:i])
                        if source:
                            json.targets.append(JSONFieldTarget(source, field.path))
                            has_sources = True

                    if has_sources:
                        container = JSONContainer(schema, json_targets)
                        action.targets.append(BodyTarget(container))
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


async def run(options: RecorderOptions) -> None:
    communications = await record(options)
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


    """
    await threads.deferToThread(chrome.kill)
    """


async def main() -> None:
    start_url = "https://43.pentest-tools.com:449/login"
    options = RecorderOptions(start_url)
    await run(options)

def main_error(failure: Failure) -> None:
    err(failure) # type: ignore[no-untyped-call]
    reactor.stop()


if __name__ == "__main__":
    d = defer.ensureDeferred(main())
    d.addErrback(main_error)
    d.addCallback(lambda *args: reactor.stop())
    reactor.run()
