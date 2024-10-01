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
import pycdp.twisted
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
EVENT_LISTENER_PATH = "./event_listener.js"

NETWORK_EVENTS = [cls for method, cls in pycdp.cdp.util._event_parsers.items() if method.startswith("Network.")]

class PyCDPListener:
    def __init__(self, cdp_session: pycdp.twisted.CDPSession, *event_types: Type[T], buffer_size=100):
        self._queue = DeferredQueue(buffer_size)
        self._closed = False
        self.network_events_count = 0

        for event_type in event_types:
            cdp_session._listeners[event_type].add(self)
    
    @property
    def closed(self):
        return self._closed

    def put(self, elem: dict):
        if self._closed: raise pycdp.twisted.CDPEventListenerClosed
        if elem.__class__ in NETWORK_EVENTS:
            self.network_events_count += 1
        self._queue.put(elem)

    def close(self):
        self._closed = True
        try:
            self._queue.put(pycdp.twisted._CLOSE_SENTINEL)
        except QueueOverflow:
            pass

    async def __aiter__(self):
        try:
            while not self._closed:
                elem = await self._queue.get()
                if elem.__class__ in NETWORK_EVENTS:
                    self.network_events_count -= 1
                if elem is pycdp.twisted._CLOSE_SENTINEL:
                    return
                yield elem
        finally:
            self._closed = True

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(buffer={len(self._queue.pending)}/{self._queue.size}, closed={self._closed})'

class AwaitableIsNotCoroutine(Exception):
    pass


def randomstr(length: int) -> str:
    return "".join(random.choices(string.printable, k=length))


def extract_origin(url: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def url_belongs_to_origin(url: str, origin: str) -> bool:
    return extract_origin(url) == extract_origin(origin)


IGNORED_EXTENSIONS = [
    ".css",
    ".jpg",
    ".js",
    ".png",
    ".svg",
    ".woff2",
]


def is_url_ignored(url: str, origin: Optional[str] = None) -> bool:
    # Ignore data URLs: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs
    if url.startswith("data:"):
        return True
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    for extension in IGNORED_EXTENSIONS:
        if path.endswith(extension):
            return True

    if origin and not url_belongs_to_origin(url, origin):
        return True

    return False


async def insert_js_leech_script(
    target_session: pycdp.twisted.CDPSession,
    expression: str,
) -> tuple[str, cdp.runtime.ExecutionContextId]:
    runtime_init_timeout = 5
    context_id = None
    context_name = randomstr(32)

    await target_session.execute(cdp.page.runtime.enable())

    receiver = None
    evt_to_listen = cdp.runtime.ExecutionContextCreated
    try:
        # Don't call target_session.listen because we need the receiver object to close it at the end
        receiver = pycdp.twisted.CDPEventListener(pycdp.twisted.DeferredQueue(1024))
        target_session._listeners[evt_to_listen].add(receiver)
        listener = aiter(receiver)

        await target_session.execute(
            cdp.page.add_script_to_evaluate_on_new_document(expression, run_immediately=True, world_name=context_name)
        )

        timed_listener = AsyncIterableWithTimeout(listener, runtime_init_timeout)
        async for evt in timed_listener:
            if evt.context.name == context_name:
                context_id = evt.context.id_
                break
    except defer.TimeoutError as exc:
        raise Exception from exc
    finally:
        if receiver is not None:
            receiver.close()

    if context_id is None:
        raise Exception

    return context_name, context_id


async def insert_js_action_listener(
    target_session: pycdp.twisted.CDPSession,
) -> tuple[str, cdp.runtime.ExecutionContextId]:
    from importlib import resources

    listener_file = resources.files(__package__) / EVENT_LISTENER_PATH
    with listener_file.open("r") as file:
        expression = file.read()

    return await insert_js_leech_script(target_session, expression)


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


class Recorder:
    def __init__(
        self,
        target_session: pycdp.twisted.CDPSession,
        urlfilter: filters.URLFilter,
        collect_all: bool,
        adblock: bool,
        start_origin: Optional[str],
    ):
        self.target_session = target_session
        self.urlfilter = urlfilter
        self.start_origin = start_origin
        self.collect_all = collect_all
        self.adblock = adblock
        self.communications: list[Union[HttpCommunication, InputAction]] = []
        self.request_map: dict[cdp.network.RequestId, HttpCommunication] = {}
        self.runtime_ctx = get_runtime_context()

    async def on_http_data(
        self,
        evt: Union[
            cdp.network.RequestWillBeSent,
            cdp.network.RequestWillBeSentExtraInfo,
            cdp.network.ResponseReceived,
            cdp.network.ResponseReceivedExtraInfo,
        ],
    ) -> None:
        if evt.request_id not in self.request_map:
            comm = HttpCommunication(evt.request_id)
            self.communications.append(comm)
            self.request_map[evt.request_id] = comm

    async def on_binding_called(self, evt: cdp.runtime.BindingCalled) -> None:
        await self.runtime_ctx.on_binding_called(evt)
        self.communications += self.runtime_ctx.pop_actions()

    async def on_execution_context_created(self, evt: cdp.runtime.ExecutionContextCreated) -> None:
        await self.runtime_ctx.on_execution_context_created(evt)

    async def on_request_will_be_sent(self, evt: cdp.network.RequestWillBeSent) -> None:
        cdp_req = evt.request
        request_id = evt.request_id

        self.request_map[request_id].add_event(evt)

        if not self.collect_all and (
            is_url_ignored(cdp_req.url, self.start_origin) or (self.adblock and self.urlfilter.should_block(evt.request.url))
        ):
            self.request_map[request_id].ignored = True

    async def on_request_will_be_sent_extra_info(self, evt: cdp.network.RequestWillBeSentExtraInfo) -> None:
        if not self.request_map[evt.request_id].ignored:
            self.request_map[evt.request_id].add_event(evt)

    async def on_response_received(self, evt: cdp.network.ResponseReceived) -> None:
        if not self.request_map[evt.request_id].ignored:
            self.request_map[evt.request_id].add_event(evt)

    async def on_response_received_extra_info(self, evt: cdp.network.ResponseReceivedExtraInfo) -> None:
        if not self.request_map[evt.request_id].ignored:
            self.request_map[evt.request_id].add_event(evt)

    async def on_loading_finished(self, evt: cdp.network.LoadingFinished) -> None:
        request_id = evt.request_id
        if request_id not in self.request_map or self.request_map[request_id].ignored:
            return

        body = None
        try:
            cdp_body_result = await self.target_session.execute(cdp.network.get_response_body(request_id))
            resulted_body, is_base_64 = cdp_body_result
            if is_base_64:
                body = base64.b64decode(resulted_body)
            else:
                body = resulted_body.encode()

        except pycdp.exceptions.CDPBrowserError as exc:
            print(exc)
            print("  --cdp-browser-error")

        self.request_map[request_id].add_event(evt)
        self.request_map[request_id].response_bodies.append(body)


async def collect_communications(
    target_session: pycdp.twisted.CDPSession,
    listener: PyCDPListener,
    urlfilter: filters.URLFilter,
    timeout: int = 120,
    collect_all: bool = False,
    adblock: bool = True,
    start_origin: Optional[str] = None,
) -> list[Union[HttpCommunication, InputAction]]:
    """Takes a cdp session, listens for events, and generates a list of
    communications.

    Might also send CDP messages to get additional info about JavaScript
    objects or HTTP body.

    Args:
        target_session: The CDP session.
        urlfilter: Tells which URLs to ignore.
        timeout: When to stop listening.

    Returns:
        A list of communications.
    """
    recorder = Recorder(target_session, urlfilter, collect_all, adblock, start_origin)
    runtime_context = get_runtime_context()
    
    timed_listener = AsyncIterableWithTimeout(aiter(listener), timeout)
    async for evt in timed_listener:
        if isinstance(evt, cdp.runtime.BindingCalled):
            await recorder.on_binding_called(evt)
        if not runtime_context.recording_running:
            break

        if isinstance(
            evt,
            (
                cdp.network.RequestWillBeSent,
                cdp.network.RequestWillBeSentExtraInfo,
                cdp.network.ResponseReceived,
                cdp.network.ResponseReceivedExtraInfo,
            ),
        ):
            await recorder.on_http_data(evt)
        if isinstance(evt, cdp.runtime.ExecutionContextCreated):
            await recorder.on_execution_context_created(evt)
        elif isinstance(evt, cdp.network.RequestWillBeSent):
            await recorder.on_request_will_be_sent(evt)
        elif isinstance(evt, cdp.network.RequestWillBeSentExtraInfo):
            await recorder.on_request_will_be_sent_extra_info(evt)
        elif isinstance(evt, cdp.network.ResponseReceived):
            await recorder.on_response_received(evt)
        elif isinstance(evt, cdp.network.ResponseReceivedExtraInfo):
            await recorder.on_response_received_extra_info(evt)
        elif isinstance(evt, cdp.network.LoadingFinished):
            await recorder.on_loading_finished(evt)

    return recorder.communications


class CDPConnection(_PyCDPConnection):
    # Remove `retry_on` wrapper from function
    connect = _PyCDPConnection.connect.__wrapped__  # type: ignore[attr-defined] # pylint: disable=no-member


# Default path: Windows
CHROME_BINARY = r"C:\Users\Marius\AppData\Local\Google\Chrome\Application\chrome.exe"
if platform.system() == "Linux":
    CHROME_BINARY = "/usr/bin/google-chrome-stable"
if platform.system() == "Darwin":
    CHROME_BINARY = r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"


@dataclass(frozen=True)
class RecorderOptions:
    start_url: str
    keep_only_same_origin_urls: bool = True
    collect_all: bool = False
    adblock: bool = True
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
        if not ret.type_ == "boolean" or ret.value is not True:
            visible_targets.append(target)
        ret, _ = await session.execute(cdp.runtime.evaluate("browser.tabs"))

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


class WidgetState:
    def __init__(self, target_session: pycdp.twisted.CDPSession):
        self.target_session = target_session

        self.start_time: Optional[float] = None
        self.stop_time: Optional[float] = None

        self.top: Optional[str] = None
        self.right: Optional[str] = None
        self.bottom: Optional[str] = None
        self.left: Optional[str] = None

    @property
    def context_id(self) -> cdp.runtime.ExecutionContextId:
        runtime_ctx = get_runtime_context()
        return runtime_ctx.widget_context_id

    async def start_timer(self) -> None:
        await self.target_session.execute(cdp.runtime.evaluate("startTimerIfElemLoaded()", context_id=self.context_id))
        self.start_time = time.time()

    async def _send_state_elapsed(self, start_time: float) -> None:
        elapsed = time.time() - start_time
        if self.stop_time is not None:
            elapsed = self.stop_time - start_time
        await self.target_session.execute(
            cdp.runtime.evaluate(f"setTimerElapsed({elapsed})", context_id=self.context_id)
        )

    async def _send_state_pos(self, top: str, right: str, bottom: str, left: str) -> None:
        # Lucky that strings are represented the same in Python and JavaScript
        expression = f"setWidgetPos({top!r}, {right!r}, {bottom!r}, {left!r})"
        await self.target_session.execute(cdp.runtime.evaluate(expression, context_id=self.context_id))

    async def send_state(self) -> None:
        if self.start_time is not None:
            await self._send_state_elapsed(self.start_time)
        if self.top is not None and self.right is not None and self.bottom is not None and self.left is not None:
            await self._send_state_pos(self.top, self.right, self.bottom, self.left)


# This function isn't used for now, because it doesn't work properly
# We use bind_func_to_context_id, instead
# Binding to context_name works first time
# But, it doesn't work when the recorder is restarted and the same Chrome tab is used
async def bind_func_to_context(
    target_session: pycdp.twisted.CDPSession, name: str, context_name: Optional[str]
) -> None:
    if context_name is None:
        return
    await target_session.execute(cdp.runtime.add_binding(name, execution_context_name=context_name))


async def bind_func_to_context_id(
    target_session: pycdp.twisted.CDPSession, name: str, context_id: Optional[cdp.runtime.ExecutionContextId]
) -> None:
    if context_id is None:
        return
    # Using execution_context_id is deprecated
    # But, adding the biding with execution_context_name doesn't work when the recorder is restarted
    #   on an already started Chrome
    await target_session.execute(cdp.runtime.add_binding(name, execution_context_id=context_id))


async def init_runtime_scripts(target_session: pycdp.twisted.CDPSession, event_listener: PyCDPListener) -> RuntimeContext:
    widget_context_name, widget_context_id = await insert_widget_extension(target_session)
    listener_context_name, listener_context_id = await insert_js_action_listener(target_session)
    await bind_func_to_context_id(target_session, RuntimeContext.TOGGLE_RECORD_BINDING, widget_context_id)
    await bind_func_to_context_id(target_session, RuntimeContext.SEND_WIDGET_POS_BINDING, widget_context_id)
    await bind_func_to_context_id(target_session, RuntimeContext.EVENT_SEND_BINDING, listener_context_id)

    widget = WidgetState(target_session)

    runtime = RuntimeContext(
        target_session,
        event_listener,
        widget_context_name,
        widget_context_id,
        listener_context_name,
        listener_context_id,
        widget,
    )

    set_runtime_context(runtime)

    return runtime


async def init_runtime_state(runtime: RuntimeContext) -> None:
    await runtime.widget.start_timer()
    await runtime.widget.send_state()


class RuntimeContext:
    TOGGLE_RECORD_BINDING = "toggleRecord"
    SEND_WIDGET_POS_BINDING = "sendWidgetPos"
    EVENT_SEND_BINDING = "sendRecordedEvent"

    def __init__(
        self,
        target_session: pycdp.twisted.CDPSession,
        event_listener: PyCDPListener,
        widget_context_name: str,
        widget_context_id: cdp.runtime.ExecutionContextId,
        listener_context_name: str,
        listener_context_id: cdp.runtime.ExecutionContextId,
        widget: WidgetState,
    ):
        self.target_session = target_session
        self.event_listener = event_listener
        self.widget_context_name = widget_context_name
        self.widget_context_id = widget_context_id
        self.listener_context_name = listener_context_name
        self.listener_context_id = listener_context_id
        self.widget = widget

        self.start_time: Optional[float] = None
        self.stop_time: Optional[float] = None

        self.actions: list[InputAction] = []

    async def on_toggle_record(self) -> None:
        if self.widget.stop_time is None:
            # Mark the time when the recording is stopped
            self.widget.stop_time = time.time()
            await self.target_session.execute(cdp.runtime.remove_binding(self.TOGGLE_RECORD_BINDING))

    async def on_send_widget_pos(self, payload: str) -> None:
        data = json.loads(payload)
        self.widget.top = data["top"]
        self.widget.right = data["right"]
        self.widget.bottom = data["bottom"]
        self.widget.left = data["left"]

    async def on_event_send(self, payload: str) -> None:
        data = json.loads(payload)

        if data["event"] == "input":
            action = InputAction(data["value"], data["selector"], data["timestamp"])
            self.actions.append(action)

    async def on_binding_called(self, evt: cdp.runtime.BindingCalled) -> None:
        if evt.name == self.TOGGLE_RECORD_BINDING:
            await self.on_toggle_record()
        elif evt.name == self.SEND_WIDGET_POS_BINDING:
            await self.on_send_widget_pos(evt.payload)
        elif evt.name == self.EVENT_SEND_BINDING:
            await self.on_event_send(evt.payload)

    async def on_execution_context_created(self, evt: cdp.runtime.ExecutionContextCreated) -> None:
        if evt.context.name == self.widget_context_name:
            self.widget_context_id = evt.context.id_
            await bind_func_to_context_id(self.target_session, self.TOGGLE_RECORD_BINDING, self.widget_context_id)
            await bind_func_to_context_id(self.target_session, self.SEND_WIDGET_POS_BINDING, self.widget_context_id)
            await self.widget.send_state()
        elif evt.context.name == self.listener_context_name:
            self.listener_context_id = evt.context.id_
            await bind_func_to_context_id(self.target_session, self.EVENT_SEND_BINDING, self.listener_context_id)

    @property
    def recording_running(self) -> bool:
        return self.widget.stop_time is None

    def pop_actions(self) -> list[InputAction]:
        actions = self.actions
        self.actions = []
        return actions


RUNTIME_CONTEXT: Optional[RuntimeContext] = None


def get_runtime_context() -> RuntimeContext:
    if RUNTIME_CONTEXT is None:
        raise RuntimeError("RUNTIME_CONTEXT is None")

    return RUNTIME_CONTEXT


def set_runtime_context(runtime_context: Optional[RuntimeContext]) -> None:
    global RUNTIME_CONTEXT
    RUNTIME_CONTEXT = runtime_context


async def insert_widget_extension(
    target_session: pycdp.twisted.CDPSession,
) -> tuple[str, cdp.runtime.ExecutionContextId]:
    from importlib import resources

    logo_file = resources.files(__package__) / LOGO_PATH
    widget_file = resources.files(__package__) / RECORDER_WIDGET_PATH

    # Construct an inline image with a data URL
    data_url = ""
    with logo_file.open("rb") as file:
        data = file.read()
        encoded = base64.b64encode(data).decode("utf-8")
        extension = LOGO_PATH.rsplit(".", maxsplit=1)[-1]
        data_url = f"data:image/{extension};base64,{encoded}"

    expression = f"""const logo_src = "{data_url}";\n"""
    with widget_file.open("r", encoding="utf8") as file:
        expression += file.read()

    return await insert_js_leech_script(target_session, expression)


async def record(options: RecorderOptions) -> list[Union[HttpCommunication, InputAction]]:
    urlfilter = filters.URLFilter()

    try:
        conn = CDPConnection(options.cdp_url, Agent(reactor), reactor)  # type: ignore[no-untyped-call]
        await conn.connect()
    except ConnectionRefusedError:
        if options.fail_if_no_connection:
            raise ConnectionRefusedError
        port = options.cdp_port
        chrome = ChromeLauncher(binary=options.binary, args=[f"--remote-debugging-port={port}", "--incognito"])
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

    # Start the listener before navigating to the page
    listener = PyCDPListener(
        target_session,
        cdp.runtime.BindingCalled,
        cdp.runtime.ExecutionContextCreated,
        cdp.network.RequestWillBeSent,
        cdp.network.RequestWillBeSentExtraInfo,
        cdp.network.ResponseReceived,
        cdp.network.ResponseReceivedExtraInfo,
        cdp.network.LoadingFinished,
        buffer_size=8192,
    )
    
    runtime = await init_runtime_scripts(target_session, listener)
    await init_runtime_state(runtime)

    if options.start_url:
        start_url = options.start_url
        await target_session.execute(cdp.page.navigate(start_url))
    else:
        info = await target_session.execute(cdp.target.get_target_info())
        # The path of this can be set with the History API
        # But the origin can't be changed
        start_url = info.url

    print("Done navigating")

    start_origin = None
    if options.keep_only_same_origin_urls:
        start_origin = extract_origin(start_url)

    try:
        communications = await collect_communications(
            target_session,
            listener,
            urlfilter,
            20,
            options.collect_all,
            options.adblock,
            start_origin
        )
    finally:
        target_session.close_listeners()
        await conn.close()

    return communications
