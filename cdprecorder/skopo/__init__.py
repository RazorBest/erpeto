from __future__ import annotations

import asyncio
import functools
import os.path
import random
import socket
import string
import subprocess
from collections import defaultdict
from typing import Callable, TYPE_CHECKING

from .._storage import DEFAULT_SOCKET_NAME, get_runtime_dir
from .sniff_protocol import (
    async_read_sock_datagram,
    ProxyEvent,
    ProxyMessage,
    RequestData,
    ResponseData,
    SniffCommand,
    SnifferError,
    SnifferMessage,
    sniffer_data_from_bytes,
    to_sock_datagram,
)

if TYPE_CHECKING:
    from asyncio import StreamReader, StreamWriter

CNT = 0


class SkopoException(Exception):
    pass


class SnifferException(SkopoException):
    def __init__(self, obj: Optional[SnifferError], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = obj


class SnifferProcessTerminated(SkopoException):
    def __init__(self, proc: asyncio.subprocess.Process, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proc = proc


class Sniffer:
    def __init__(self):
        self._ignore_reconnects = False
        self.session_to_msg_queues = defaultdict(asyncio.Queue)

    def ignore_reconnects(self, ignore=True):
        self._ignore_reconnects = ignore

    async def _get_data(self) -> bytes:
        raise NotImplementedError

    async def pushback_message(self, obj):
        await self.session_to_msg_queues[obj.session].put(obj)

    def _handle_message(self, obj, ignore_error: bool = False, session: Optional[int] = None) -> Optional[ProxyMessage]:
        if isinstance(obj, SnifferError) and not ignore_error:
            raise ProxyException(obj)

        if self._ignore_reconnects and isinstance(obj, ProxyEvent):
            if obj.event == ProxyEvent.CONNECT or obj.event == ProxyEvent.CLOSE:
                return None

        if isinstance(obj, SnifferMessage):
            if obj.session is None and session is not None:
                raise ProxyException(obj, "Received sesionless message in a context with session")
            if session is not None and obj.session != session:
                self.pushback_message(obj)
                return None

        # TODO: check if it's a bug it this returns when session is None, but obj.session is not None
        return obj

    async def get_message(self, ignore_error: bool = False, session: Optional[int] = None) -> ProxyMessage:
        if session is not None:
            while True:
                t1 = asyncio.create_task(self.session_to_msg_queues[session].get())
                t2 = asyncio.create_task(self._get_data())
                done, pending = await asyncio.wait([t1, t2], return_when=asyncio.FIRST_COMPLETED)
                for t in pending:
                    t.cancel()

                results = []
                if t1 in done:
                    results.append(t1.result())
                if t2 in done:
                    data = t1.result()
                    obj, _ = sniffer_data_from_bytes(data)
                    results.append(obj)

                while results:
                    obj = results.pop(0)
                    obj = self._handle_message(obj, ignore_error, session)
                    if obj is not None:
                        for result in results:
                            self.pushback_message(result)
                        return obj

        while True:
            data = await self._get_data()
            obj, _ = sniffer_data_from_bytes(data)
            obj = self._handle_message(obj, ignore_error, session)
            if obj is not None:
                return obj

    async def get_request_data(self, ignore_error: bool = False, session: Optional[int] = None) -> RequestData:
        while True:
            msg = await self.get_message(ignore_error, session)
            if not isinstance(msg, RequestData):
                raise SnifferException(msg, "Expected message of type RequestData")
            return msg

    async def get_response_data(self, ignore_error: bool = False, session: Optional[int] = None) -> ResponseData:
        while True:
            msg = await self.get_message(ignore_error, session)
            if not isinstance(msg, ResponseData):
                raise SnifferException(msg, "Expected message of type ResponseData")
            return msg

    async def get_proxy_event(self, ignore_error: bool = False, session: Optional[int] = None) -> ProxyEvent:
        while True:
            msg = await self.get_message(ignore_error, session)
            if not isinstance(msg, ProxyEvent):
                raise SnifferException(msg, "Expected message of type ProxyEvent")
            return msg

    async def wait_event(self, event_id: int, ignore_error: bool = False, session: Optional[int] = None) -> ProxyEvent:
        while True:
            msg = await self.get_message(ignore_error, session)
            if not isinstance(msg, ProxyEvent):
                raise SnifferException(msg, "Expected message of type ProxyEvent")
            if msg.event != event_id:
                raise SnifferException(msg, f"Expected event id {event_id}")

            return msg

    async def _send_data(self, data: bytes):
        raise NotImplementedError

    async def send_command(
        self,
        command: int,
        request: Optional[RequestData] = None,
        response: Optional[ResponseData] = None,
        session: Optional[int] = None,
    ):
        sniff_command = SniffCommand(command, request, response)
        sniff_command.session = session
        data = sniff_command.to_bytes()
        await self._send_data(data)

    async def send_error(self, msg: SnifferError, session: Optional[int] = None):
        msg.session = session
        data = msg.to_bytes()
        await self._send_data(data)

    async def async_stop(self):
        raise NotImplemented

    def to_session(self, session: int):
        return SnifferSession(self, session)


class SnifferSession:
    def __init__(self, sniffer: Sniffer, id_: int):
        self.sniffer = sniffer
        self.id = id_

    def __getattr__(self, key: str):
        value = getattr(self.sniffer, key)
        if isinstance(value, Callable):
            value = functools.partial(value, session=self.id)

        return value


class ComparatorSniffer:
    def __init__(self, sniffer1: Sniffer, sniffer2: Sniffer, on_diff: Callable):
        self.sniffer1 = sniffer1
        self.sniffer2 = sniffer2

        self.on_diff = on_diff

        # self.http_queues = defaultdict(lambda _: asyncio.Queue(), asyncio.Queue())
        self.sessions1 = defaultdict(lambda _: asyncio.Queue())
        self.sessions2 = defaultdict(lambda _: asyncio.Queue())
        self.unpaired_sessions1 = {}
        self.unpaired_sessions2 = {}
        self.waiting_tasks = []

    async def handle_request_response(self, task, queue1: asyncio.Queue, queue2: asyncio.Queue):
        session1 = self.sniffer1
        session2 = self.sniffer2

        req1 = await queue1.get()
        assert isinstance(req1, RequestData)
        if req1.session is not None:
            session1 = session1.to_session(req1.session)
        await session1.send_command(SniffCommand.NOP)

        req2 = await queue2.get()
        assert isinstance(req2, RequestData)

        if req1 != req2:
            self.on_diff(req1, req2)

        if req2.session is not None:
            session2 = self.sniffer2.to_session(req2.session)
        await session2.send_command(SniffCommand.REPLACE, response=res1)

        res1 = await queue1.get()
        assert isinstance(res1, ResponseData)
        await session1.send_command(SniffCommand.NOP)

        res2 = await queue2.get()
        assert isinstance(res2, ResponseData)

        # If the proxy works as expected, this should never happen
        if res1 != res2:
            self.on_diff(res1, res2)
        await session2.send_command(SniffCommand.NOP)

    @staticmethod
    def _request_data_key(obj: RequestData) -> str:
        return obj.method + url

    @staticmethod
    async def _try_extracting_session(obj: RequestData, unpaired_sessions: dict) -> Optional[asyncio.Queue]:
        obj_key = self._request_data_key(obj)
        if obj_key in unpaired_sessions:
            value = unpaired_sessions[obj_key]
            del unpaired_sessions[obj_key]
            return value

        return value

    async def _create_comparator_task(self, q1: asyncio.Queue, q2: asyncio.Queue):
        task = asyncio.create_task(handle_request_response(q1, q2))
        self.waiting_tasks.append((task, q1, q2))
        return task

    async def run(self):
        print("Comparator start run")
        on_message1 = asyncio.create_task(self.sniffer1.get_message())
        on_message2 = asyncio.create_task(self.sniffer2.get_message())
        while True:
            print("Comparator await")
            done, pending = await asyncio.wait([on_message1, on_message2], return_when=asyncio.FIRST_COMPLETED)
            print("Comparator callback")

            for done_task in done:
                obj = done_task.result()
                print(f"ComparatorSniffer object: {obj}")
                if not isinstance(obj, (RequestData, ResponseData)):
                    logging.error("Received unwanted object: %s", obj)
                    continue

                object_id = obj.meta.object_id

                if done_task is on_message1:
                    if obj.session not in self.sessions1:
                        q1 = asyncio.Queue()
                        self.sessions1[obj.session] = q1
                        q2 = self._try_extracting_session(obj, self.unpaired_sessions2)
                        if q2 is not None:
                            self._create_comparator_task(q1, q2)

                    q1 = self.sessions1[obj.session]
                    await q1.put(obj)
                    on_message1 = asyncio.create_task(self.sniffer1.get_message())

                if done_task is on_message2:
                    if obj.session not in self.sessions2:
                        q2 = asyncio.Queue()
                        self.sessions2[obj.session] = q2
                        q1 = self._try_extracting_session(obj, self.unpaired_sessions1)
                        if q1 is not None:
                            self._create_comparator_task(q1, q2)

                    q2 = self.sessions2[obj.session]
                    await q2.put(obj)
                    on_message2 = asyncio.create_task(self.sniffer2.get_message())

    def stop(self):
        self.sniffer1.stop()
        self.sniffer2.stop()


async def mitmproxy_run(
    sniffer_socket_address: str,
    host: str = "localhost",
    port: int = 8080,
    addon_script: str = "intercept_addon.py",
    binary: str = "mitmdump",
):
    proxy_name: str = "".join(random.choices(string.ascii_letters, k=32))
    module_dir = os.path.dirname(os.path.realpath(__file__))
    addon_path = os.path.join(module_dir, addon_script)
    cli_args = [
        "--mode",
        "regular",
        "--listen-host",
        host,
        "--listen-port",
        str(port),
        "-s",
        addon_path,
        "--set",
        f"socketaddress={sniffer_socket_address}",
        "--set",
        f"proxyname={proxy_name}",
    ]
    args = [binary] + cli_args

    # TODO: stderr DEVNULL
    p = await asyncio.create_subprocess_exec(*args)  # , stdout=subprocess.PIPE)

    return p, host, port, proxy_name


class MitmproxySniffer(Sniffer):
    def __init__(
        self,
        sockaddr: str,
        proxy_host: str,
        proxy_port: int,
        proxy_name: str,
        mitmproxy_proc: asyncio.subprocess.Process,
    ):
        super().__init__()
        self.sockaddr = sockaddr
        self._server = None
        self.stop_event = asyncio.Event()

        self._read_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._write_queue: asyncio.Queue[bytes] = asyncio.Queue()

        self._proc = mitmproxy_proc
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_name = proxy_name

    async def init(self):
        self._server = await asyncio.start_unix_server(self.on_client_connected, path=self.sockaddr)

    @property
    def proxy_url(self):
        return f"http://{self.proxy_host}:{self.proxy_port}"

    async def _get_data(self):
        wait_task = asyncio.create_task(self._proc.wait())
        read_task = asyncio.create_task(self._read_queue.get())
        try:
            done, _pending = await asyncio.wait([wait_task, read_task], return_when=asyncio.FIRST_COMPLETED)
        finally:
            # Here, I found out that task cancelation can create bugs
            # Hence, in a couroutine, you should always expect that when you
            #   await a coroutine/task, that can generate a CancelledError.
            wait_task.cancel()
            read_task.cancel()

        if wait_task in done:
            print("Sniffer proxy error")
            raise SnifferProcessTerminated(None, self._proc)

        return read_task.result()

    async def _send_data(self, data: bytes):
        datagram = to_sock_datagram(data)
        print(f"Sniffer._send_data: {data}")
        await self._write_queue.put(datagram)
        print(f"done put")

    async def on_client_connected(self, reader: StreamReader, writer: StreamWriter):
        global CNT
        """Called when a proxy server has connected to this sniffer."""
        print(f"On client connected")
        await self._read_queue.put(ProxyEvent(event=ProxyEvent.CONNECT).to_bytes())

        # Handle both reading and writing concurrently
        # Listen on the reader stream and the internal write queue
        task1 = asyncio.create_task(async_read_sock_datagram(reader))
        task2 = asyncio.create_task(self._write_queue.get())
        stop_task = asyncio.create_task(self.stop_event.wait())
        print(f"Created task2 for awaiting {self._write_queue}")
        try:
            while True:
                # ignore pending tasks, because they will be waited again in the next loop iteration
                done, _pending = await asyncio.wait([task1, task2, stop_task], return_when=asyncio.FIRST_COMPLETED)

                if stop_task in done:
                    return

                if task1 in done:
                    data = task1.result()
                    await self._read_queue.put(data)
                    # recreate the task
                    task1 = asyncio.create_task(async_read_sock_datagram(reader))

                if task2 in done:
                    data = task2.result()
                    print(f"Sniffer writes data: {data}")
                    writer.write(data)
                    await writer.drain()
                    # recreate the task
                    task2 = asyncio.create_task(self._write_queue.get())
        except asyncio.exceptions.IncompleteReadError:
            pass
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"Exception: {e}")
            # Hopefully, the event loop is still running
            await self._read_queue.put(ProxyEvent(event=ProxyEvent.CLOSE).to_bytes())
            while not self._write_queue.empty():
                await self._write_queue.get()
            raise
        finally:
            task1.cancel()
            task2.cancel()
            stop_task.cancel()

        await self._read_queue.put(ProxyEvent(event=ProxyEvent.CLOSE).to_bytes())

        print(f"on_client_connected: return")

    def stop(self):
        if self._server is not None:
            self._server.close()
            self.stop_event.set()
            self._server = None
        print("Stopping")
        if self._proc is None:
            return

        self._proc.terminate()
        print("Terminate")
        try:
            # Imagine having an API that that has both async and blocking functions
            # Sadly, this is not the case for asyncio.subprocess.Process
            print("Waiting")
            p = self._proc._transport._proc.wait(timeout=0.5)
            print("Waited")
        except subprocess.TimeoutExpired:
            print("Killing")
            self._proc.kill()

        print("Done stopping")

        self._proc = None

    def __del__(self):
        print(f"Called del for {self}")
        # The object might be destroyed before __init__ terminates
        if hasattr(self, "_proc"):
            self.stop()


async def create_mitmproxy_sniffer_comparator(
    on_diff: Callable, socksuffix1: str = "1", proxy_port1: int = 8080, socksuffix2: str = "2", proxy_port2: int = 8081
) -> ComparatorSniffer:
    if socksuffix1 == socksuffix2:
        raise SnifferException("Socket suffixes must be different")
    if proxy_port1 == proxy_port2:
        raise SnifferException("Proxy ports must be different")

    sockaddr1 = os.path.join(get_runtime_dir(), DEFAULT_SOCKET_NAME + socksuffix1)
    proc1, host1, port1, proxy_name1 = await mitmproxy_run(sockaddr1, port=proxy_port1)
    sniffer1 = MitmproxySniffer(sockaddr1, host1, port1, proxy_name1, proc1)

    sockaddr2 = os.path.join(get_runtime_dir(), DEFAULT_SOCKET_NAME + socksuffix2)
    proc2, host2, port2, proxy_name2 = await mitmproxy_run(sockaddr2, port=proxy_port2)
    sniffer2 = MitmproxySniffer(sockaddr2, host2, port2, proxy_name2, proc2)

    await sniffer1.init()
    await sniffer2.init()

    try:
        await sniffer1.wait_event(ProxyEvent.CONNECT)
        await sniffer2.wait_event(ProxyEvent.CONNECT)
    except:
        proc1.kill()
        out, err = await proc1.communicate()
        print(f"Proc output: {out}")
        print(f"Proc err: {err}")
        raise

    print("The sniffers are ready to start")

    sniffer1.ignore_reconnects(True)
    sniffer2.ignore_reconnects(True)
    comparator = ComparatorSniffer(sniffer1, sniffer2, on_diff)

    return comparator
