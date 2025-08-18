from __future__ import annotations

import asyncio
import os
import pickle
import queue
import socket
import sys
import threading
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .._storage import get_runtime_dir, DEFAULT_SOCKET_NAME
from .. import logger
from . import mitm_runner, common_data
from .common_data import RequestData, ResponseData


if TYPE_CHECKING:
    import subprocess
    from asyncio.events import AbstractEventLoop
    from typing import Any, Callable, Coroutine, Generic, Optional, TypeVar

    T = TypeVar("T")


# for pickle to find the module
# Reference: https://stackoverflow.com/questions/2121874/python-pickling-after-changing-a-modules-directory
sys.modules["common_data"] = common_data


class SnifferException(Exception):
    pass


def asyncio_run_coroutine_threadsafe(coro: Coroutine) -> None:
    asyncio.run_coroutine_threadsafe(coro, asyncio.get_event_loop())


class ThreadsafeAsyncWaker:
    def __init__(self, loop: AbstractEventLoop, callback: Callable[[], Any]):
        self.loop = loop
        self.callback = callback

    def wake(self) -> None:
        asyncio.run_coroutine_threadsafe(self.callback(), self.loop)


class ThreadSafeAsyncQueue(Generic[T]):
    def __init__(self, size: int, loop: Optional[AbstractEventLoop] = None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._tqueue: queue.Queue[T] = queue.Queue(size)
        self._aqueue: asyncio.Queue[T] = asyncio.Queue(size)
        self._async_waker = ThreadsafeAsyncWaker(loop, self.transfer_to_async)

    async def transfer_to_async(self) -> None:
        try:
            item = self._tqueue.get(block=False)
            await self._aqueue.put(item)
        except queue.Empty:
            pass

    def put(self, item: T) -> None:
        self._tqueue.put(item)
        self._async_waker.wake()

    def get(self) -> T:
        return self._tqueue.get()

    async def async_put(self, item: T) -> None:
        await self._aqueue.put(item)
        try:
            item = await self._aqueue.get_nowait()
            # TODO: This might block :(
            self._tqueue.put(item)
        except asyncio.QueueEmpty:
            pass

    async def async_get(self) -> T:
        return await self._aqueue.get()


class CrossThreadSnifferBase:
    """Thread safe methods used by the Sniffer class."""

    def __init__(self, loop: Optional[AbstractEventLoop] = None):
        self.lock = threading.Lock()
        self.signal_queue = None
        if loop is not None:
            self.signal_queue = ThreadSafeAsyncQueue(0, loop)
        self.httpobj_queue = None
        self.modification_queue = queue.Queue(maxsize=1)

        self.client_connected = False

    def set_httpobj_queue(self, httpobj_queue: queue.Queue):
        with self.lock:
            self.httpobj_queue = httpobj_queue

    def publish_httpobj(self, httpobj):
        if self.httpobj_queue is None:
            return
        self.httpobj_queue.put((self, httpobj))

    def get_modification(self):
        return self.modification_queue.get()

    def publish_modification(self, obj: object):
        self.modification_queue.put(obj)

    def send_signal(self, signal):
        self.signal_queue.put(signal)


class Sniffer(CrossThreadSnifferBase):
    SIG_CLIENT_CONNECTED = 1

    def __init__(self, coroutine_runner=None, coroutine_runner_threadsafe=None, sock_suffix: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        if coroutine_runner is not None:
            self.coroutine_runner = coroutine_runner
        else:
            self.coroutine_runner = asyncio.run
        if coroutine_runner_threadsafe is not None:
            self.coroutine_runner_threadsafe = coroutine_runner_threadsafe
        else:
            self.coroutine_runner_threadsafe = asyncio_run_coroutine_threadsafe

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.running = False

        dirpath = get_runtime_dir()
        self.sockpath = os.path.join(dirpath, DEFAULT_SOCKET_NAME + sock_suffix)
        # Try to delete the socket if it already exists
        try:
            os.unlink(self.sockpath)
        except FileNotFoundError:
            pass

        self._id_counter = 0
        self.client_connected = False

    def run(self) -> None:
        self.coroutine_runner(self._async_run())

    async def on_client_connected(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        if self.client_connected:
            raise SnifferException("Sniffer only supports one client at a time")
        self.client_connected = True
        self.send_signal(self.SIG_CLIENT_CONNECTED)
        try:
            print("Client connected")
            conn = common_data.AsyncioSniffConnection(reader, writer)
            try:
                try:
                    proxyname = await conn.read_str()
                except common_data.SniffProtocolException as exc:
                    raise SnifferException from exc

                print(f"Proxy name: {proxyname}")
                while True:
                    try:
                        httpobj = await conn.read_httpobj()
                    except common_data.SniffProtocolException as exc:
                        raise SnifferException from exc

                    print(f"Got {httpobj}")

                    # Yes, the calls to Queue can block the thread, that's
                    #   why we allow only one client connection at a time
                    self.publish_httpobj(httpobj)
                    modification = self.get_modification()

                    req, resp = modification

                    if resp is not None:
                        await conn.send("REPLACE_RESPONSE")
                        await conn.send(resp)
                    elif req is not None and not isinstance(httpobj, ResponseData):
                        await conn.send("REPLACE_REQUEST")
                        await conn.send(req)
                    else:
                        await conn.send("OK")
            except asyncio.IncompleteReadError:
                pass

            print("Client done")
        except Exception as exc:
            print(f"Sniffer Exception: {exc}")
            import traceback

            traceback.print_exception(exc)
            raise
        finally:
            self.client_connected = False

    async def _async_run(self):
        try:
            os.unlink(self.sockpath)
        except FileNotFoundError:
            pass
        self.server = await asyncio.start_unix_server(self.on_client_connected, self.sockpath)
        await self.server.serve_forever()

    async def _async_stop(self):
        self.server.close()

    def stop(self) -> None:
        self.coroutine_runner_threadsafe(self._stop())


class SnifferThreadCombiner:
    """Combines sniffers from different threads and makes them accessible
    from a single thread."""

    async def __init__(self, sniffers: list[Sniffer]):
        self.sniffers = sniffers
        self.read_queue = ThreadSafeAsyncQueue(0, asyncio.get_event_loop())

        for sniffer in self.sniffers:
            sniffer.set_httpobj_queue(self.read_queue)

    async def get_message(self):
        return await self.read_queue.async_get()

    async def send_message(self, sniffer, obj: object):
        sniffer.modification_queue.put(obj)


# TODO: The sniffer comparator should better have references to the sniffers
class SnifferComparator:
    def __init__(self, on_fail, sniffer1: Sniffer, sniffer2: Sniffer, event_loop=None):
        self.on_fail = on_fail

        """
        self.req1 = None
        self.req2 = None
        self.res1 = None
        self.request1_ready = asyncio.Semaphore(0)
        self.request2_ready = asyncio.Semaphore(0)
        self.requests_ready = asyncio.Semaphore(0)

        self.request1_lock = asyncio.Lock()
        self.request2_lock = asyncio.Lock()
        """

        self.requests_passed = 0

        self.sniffer1 = sniffer1
        self.sniffer2 = sniffer2

        self.sniffer1_httpobj_queue = ThreadSafeAsyncQueue(0, event_loop)
        self.sniffer2_httpobj_queue = ThreadSafeAsyncQueue(0, event_loop)

        sniffer1.set_httpobj_queue(self.sniffer1_httpobj_queue)
        sniffer2.set_httpobj_queue(self.sniffer2_httpobj_queue)
        # self.combiner = SnifferThreadCombiner([sniffer1, sniffer2])
        self.running = False

    async def run(self):
        self.running = True
        while self.running:
            _, req1 = await self.sniffer1_httpobj_queue.async_get()
            print("Got req1")
            if not isinstance(req1, RequestData):
                raise SnifferException("Expected RequestData from sniffer1")

            _, req2 = await self.sniffer2_httpobj_queue.async_get()
            print("Got req2")
            if not isinstance(req2, RequestData):
                raise SnifferException("Expected RequestData from sniffer2")

            if req1 != req2:
                print("Calling on_fail")
                await self.on_fail(self, req1, req2)

            self.sniffer1.publish_modification((None, None))
            _, res1 = await self.sniffer1_httpobj_queue.async_get()
            self.sniffer1.publish_modification((None, None))
            if not isinstance(res1, ResponseData):
                raise SnifferException("Expected RespsoneData from sniffer1")

            self.sniffer2.publish_modification((None, res1))
            _, res2 = await self.sniffer2_httpobj_queue.async_get()
            if not isinstance(res2, ResponseData):
                raise SnifferException("Expected RespsoneData from sniffer2")

            if res1 != res2:
                print("Expected the safe response from sniffer2")
                self.on_fail(self, res1, res2)

            self.sniffer2.publish_modification((None, None))

            self.requests_passed += 1

            print("Done comparator iteration")

    async def on_request1(self, req: RequestData):
        print("Got request1")
        async with self.request1_lock:
            self.req1 = req
            self.request1_ready.release()
            print("Released req1_ready")
            await self.request2_ready.acquire()

            print("Barrier released")

            if self.req1 != self.req2:
                print("Calling on_fail")
                self.on_fail(self.req1, self.req2)

            return None, None

            self.req1 = None

    async def on_request2(self, req: RequestData):
        print("Got request2")
        async with self.request2_lock:
            self.req2 = req
            self.request2_ready.release()

            print("Released req2_ready")

            await self.requests_ready.acquire()
            print("Got response for req2")
            self.req2 = None

            return None, self.res1

    async def on_response1(self, res: ResponseData):
        print("Got response1")
        # Assume on_request1 was called for the corresponding request
        self.res1 = res
        print("Well, nice")
        self.requests_ready.release()
        print("Released")

    async def on_response2(self, res: ResponseData):
        print("On response2 was called but this should never happen")


@dataclass
class ProxyInfo:
    proc: subprocess.Popen
    host: str
    port: int
    name: str


class MitmproxySnifferManager:
    def __init__(self, sock_suffix: str, event_loop=None):
        if event_loop is None:
            event_loop = asyncio.get_event_loop()
        self.sniffer = Sniffer(
            sock_suffix=sock_suffix,
            loop=event_loop,
        )
        self.thread = None

        self.proxies = {}

    def start_sniffer_on_thread(self):
        if self.thread is not None:
            raise SnifferException("Sniffer thread already started")

        self.sniffer.running = True
        self.thread = threading.Thread(target=self.sniffer.run, daemon=True)
        self.thread.start()
        # Wait for the sniffer to open the listening socket
        time.sleep(0.5)

    def start_proxy_instance(self, host=None, port=None):
        if self.thread is None:
            raise SnifferException("Sniffer must be started before starting a proxy")

        kwargs = {}
        if host is not None:
            kwargs["host"] = host
        if port is not None:
            kwargs["port"] = port

        proc, host, port, proxy_name = mitm_runner.run(self.sniffer.sockpath, **kwargs)

        self.proxies[proxy_name] = ProxyInfo(
            proc=proc,
            host=host,
            port=port,
            name=proxy_name,
        )

        return self.proxies[proxy_name]

    async def wait_for_proxy_connection_with_sniffer(self):
        while True:
            sig = await self.sniffer.signal_queue.async_get()
            print(f"Got signal on queue: {sig}")
            if sig is self.sniffer.SIG_CLIENT_CONNECTED:
                break

    def stop_from_thread(self):
        self.sniffer.stop()
        self.thread.join()

    def stop_proxy_instance(self, proxy_name: str):
        try:
            proxy_info = self.proxies[proxy_name]
        except KeyError:
            raise SnifferException(f"No proxy with the name: {proxy_name!r}")

        proxy_info.proc.stop()
        del self.proxies[proxy_name]

    def __del__(self):
        for proxy in self.proxies.values():
            proxy.proc.terminate()

        self.proxies.clear()
