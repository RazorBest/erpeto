from __future__ import annotations

from typing import cast, Optional, Union, TYPE_CHECKING

import pycdp
import requests
import twisted.internet.reactor

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
from cdprecorder.recorder import (
    HttpCommunication,
    RecorderOptions,
    record,
)

import cdprecorder.analyser

if TYPE_CHECKING:
    from pycdp.cdp.util import T_JSON_DICT
    from twisted.python.failure import Failure

    from cdprecorder.type_checking import CdpEvent, HttpTarget


# https://github.com/twisted/twisted/issues/9909
reactor = cast(IReactorCore, twisted.internet.reactor)


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


def _generate_events_with_redirects_extracted(events: list[CdpEvent]) -> list[CdpEvent]:
    new_events = []
    future_events: list[CdpEvent] = []
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
    

def parse_communications_into_actions(communications: list[Union[HttpCommunication, InputAction]]) -> list[BrowserAction]:
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
            info_str += str(getattr(evt, "method", getattr(getattr(evt, "request", None), "method", None))) + " "
            info_str += str(getattr(getattr(evt, "request", None), "url", None)) + " "
            
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

                type_ = evt.type_ if hasattr(evt, "type_") else None
                curr_request = RequestAction(type_=type_)
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



def merge_input_actions(actions: list[BrowserAction]) -> list[BrowserAction]:
    new_actions = []
    
    prev_input = None
    index = 0
    
    for action in actions:
        if not isinstance(action, InputAction):
            new_actions.append(action)
            continue
        
        print(f"Input action: {action.text} ----- {action.selector}", )
        
        if prev_input is not None and prev_input.selector != action.selector:
            new_actions.append(prev_input)
        prev_input = action
        # The position of the action, if it was to be added now
        index = len(new_actions)
    
    if prev_input is not None:
        new_actions.insert(index, prev_input)
    
    return new_actions
        

async def run(options: RecorderOptions) -> None:
    communications = await record(options)
    actions = parse_communications_into_actions(communications)
    make_action_ids_consecutive_from_list(actions)
    actions = merge_input_actions(actions)
    cdprecorder.analyser.analyse_actions(actions)
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
    start_url = "https://github.com"
    options = RecorderOptions(start_url)
    #options = RecorderOptions(start_url, collect_all=True)
    await run(options)

def main_error(failure: Failure) -> None:
    err(failure) # type: ignore[no-untyped-call]
    reactor.stop()


if __name__ == "__main__":
    d = defer.ensureDeferred(main())
    d.addErrback(main_error)
    d.addCallback(lambda *args: reactor.stop())
    reactor.run()
