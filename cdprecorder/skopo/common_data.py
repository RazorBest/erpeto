from __future__ import annotations

import socket
import pickle
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import asyncio
    from typing import Union


class RequestData:
    __slots__ = ("http_version", "method", "url", "headers", "raw_content", "trailers", "object_id")

    def __init__(
        self,
        http_version: str,
        method: str,
        url: str,
        headers: list[tuple[str, str]],
        raw_content: bytes,
        trailers: list[tuple[str, str]],
        object_id: int,
    ):
        self.http_version = http_version
        self.method = method
        self.url = url
        self.headers = headers
        self.raw_content = raw_content
        self.trailers = trailers
        self.object_id = object_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RequestData):
            raise ValueError("Value must RequestData instance")
        # Compares everything but object_id
        attr1 = (self.http_version, self.method, self.url, self.headers, self.raw_content, self.trailers)
        attr2 = (other.http_version, other.method, other.url, other.headers, other.raw_content, other.trailers)

        return attr1 == attr2

    def __str__(self) -> str:
        text = f"{self.__class__.__name__}("
        text += f"http_version={self.http_version}, "
        text += f"method={self.method}, "
        text += f"url={self.url}, "
        text += f"headers={self.headers}, "
        text += f"raw_content={self.raw_content!r}, "
        text += f"trailers={self.trailers}, "
        text += f"object_id={self.object_id}"
        text += ")"

        return text


class ResponseData:
    __slots__ = ("http_version", "status_code", "reason", "headers", "raw_content", "trailers", "object_id")

    def __init__(
        self,
        http_version: str,
        status_code: int,
        reason: str,
        headers: list[tuple[str, str]],
        raw_content: bytes,
        trailers: list[tuple[str, str]],
        object_id: int,
    ):
        self.http_version = http_version
        self.status_code = status_code
        self.reason = reason
        self.headers = headers
        self.raw_content = raw_content
        self.trailers = trailers
        self.object_id = object_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResponseData):
            raise ValueError("Value must ResponseData instance")
        # Compares everything but object_id
        attr1 = (self.http_version, self.status_code, self.reason, self.headers, self.raw_content, self.trailers)
        attr2 = (other.http_version, other.status_code, other.reason, other.headers, other.raw_content, other.trailers)

        return attr1 == attr2


class SniffProtocolException(Exception):
    pass


class SniffProtocol:
    def to_datagram(self, sendable_obj: Union[str, RequestData, ResponseData]) -> bytes:
        assert isinstance(sendable_obj, (str, RequestData, ResponseData))
        body = pickle.dumps(sendable_obj)
        size = len(body)
        data = size.to_bytes(8, byteorder="big") + body

        return data


class SniffConnection:
    def __init__(self, sockaddr: str):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(sockaddr)
        self.protocol = SniffProtocol()

    def send(self, sendable_obj: Union[RequestData, ResponseData]) -> None:
        data = self.protocol.to_datagram(sendable_obj)
        self.sock.send(data)

    def read(self) -> object:
        size_data = self.sock.recv(8)
        size = int.from_bytes(size_data, "big")
        data = self.sock.recv(size)

        obj = pickle.loads(data)
        if not isinstance(obj, (str, RequestData, ResponseData)):
            raise SniffProtocolException(f"sendable_obj is of unsupported type {type(obj)}")

        return obj

    def read_str(self) -> str:
        obj = self.read()
        if not isinstance(obj, str):
            raise SniffProtocolException(f"Object is of type {type(obj)}. Expected {str}")

        return obj

    def read_httpobj(self) -> Union[RequestData, ResponseData]:
        obj = self.read()
        if not isinstance(obj, (RequestData, ResponseData)):
            raise SniffProtocolException(f"Object is of type {type(obj)}. Expected {(RequestData, ResponseData)}")

        return obj

    def read_request_data(self) -> RequestData:
        obj = self.read()
        if not isinstance(obj, RequestData):
            raise SniffProtocolException(f"Object is of type {type(obj)}. Expected {RequestData}")

        return obj

    def read_response_data(self) -> ResponseData:
        obj = self.read()
        if not isinstance(obj, ResponseData):
            raise SniffProtocolException(f"Object is of type {type(obj)}. Expected {ResponseData}")

        return obj

    def close(self) -> None:
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


class AsyncioSniffConnection:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.protocol = SniffProtocol()

    async def send(self, sendable_obj: Union[RequestData, ResponseData]) -> None:
        data = self.protocol.to_datagram(sendable_obj)
        self.writer.write(data)
        await self.writer.drain()

    async def read(self) -> object:
        size_data = await self.reader.readexactly(8)
        size = int.from_bytes(size_data, "big")
        data = await self.reader.readexactly(size)

        obj = pickle.loads(data)
        if not isinstance(obj, (str, RequestData, ResponseData)):
            raise SniffProtocolException(f"Object is of unsupported type {type(obj)}")

        return obj

    async def read_str(self) -> str:
        obj = await self.read()
        if not isinstance(obj, str):
            raise SniffProtocolException(f"Object is of type {type(obj)}. Expected {str}")

        return obj

    async def read_httpobj(self) -> Union[RequestData, ResponseData]:
        obj = await self.read()
        if not isinstance(obj, (RequestData, ResponseData)):
            raise SniffProtocolException(f"Object is of type {type(obj)}. Expected {(RequestData, ResponseData)}")

        return obj

    async def read_request_data(self) -> RequestData:
        obj = await self.read()
        if not isinstance(obj, RequestData):
            raise SniffProtocolException(f"Object is of type {type(obj)}. Expected {RequestData}")

        return obj

    async def read_response_data(self) -> ResponseData:
        obj = await self.read()
        if not isinstance(obj, ResponseData):
            raise SniffProtocolException(f"Object is of type {type(obj)}. Expected {ResponseData}")

        return obj
