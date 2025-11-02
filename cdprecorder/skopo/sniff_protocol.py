from __future__ import annotations

import asyncio
import functools
import os.path
import subprocess
from collections import defaultdict
from enum import IntEnum
from typing import Callable, TYPE_CHECKING


if TYPE_CHECKING:
    import socket
    from asyncio import StreamReader, StreamWriter
    from typing import Optional, TypeAlias, Protocol, Union


def bytes_to_varlen_bytes(data: bytes) -> bytes:
    size = len(data)
    return size.to_bytes(8, "big") + data


class SnifferMessageType(IntEnum):
    REQUEST_DATA = 1
    RESPONSE_DATA = 2
    PROXY_EVENT = 3
    SNIFF_COMMAND = 4
    SNIFFER_ERROR = 5
    INT64 = 6
    STRING = 7
    NONE = 8


class SnifferNone:
    @staticmethod
    def to_bytes() -> bytes:
        data = b""
        data += SnifferMessageType.NONE.to_bytes(8, "big")
        return data


class SnifferInt64:
    @staticmethod
    def to_bytes(value: Optional[int]) -> bytes:
        if value is None:
            return SnifferNone.to_bytes()

        data = b""
        data += SnifferMessageType.INT64.to_bytes(8, "big")
        data += value.to_bytes(8, "big")
        return data


class SnifferString:
    @staticmethod
    def to_bytes(value: Optional[str]) -> bytes:
        if value is None:
            return SnifferNone.to_bytes()
        
        data = b""
        data += SnifferMessageType.STRING.to_bytes(8, "big")
        data += bytes_to_varlen_bytes(value.encode())

        return data
    
    @staticmethod
    def from_bytes(data: bytes) -> tuple[str, int]:
        i = 0
        message_type = int.from_bytes(data[i : i + 8], "big")
        i += 8
        assert message_type == SnifferMessageType.STRING

        length = int.from_bytes(data[i : i + 8], "big")
        i += 8

        s = data[i : i + length].decode("utf-8")
        i += length

        return s, i + length


class SnifferMetadata:
    def __init__(self, object_id: int, timestamp: int, proxyname: str) -> None:
        self.object_id = object_id
        self.timestamp = timestamp
        self.proxyname = proxyname

    def to_bytes(self) -> bytes:
        data = b""
        data += self.object_id.to_bytes(8, "big")
        data += self.timestamp.to_bytes(8, "big")
        data += bytes_to_varlen_bytes(self.proxyname.encode())

        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> tuple[SnifferMetadata, int]:
        i = 0
        object_id = int.from_bytes(data[i : i + 8], "big")
        i += 8

        timestamp = int.from_bytes(data[i : i + 8], "big")
        i += 8

        size = int.from_bytes(data[i : i + 8], "big")
        i += 8

        proxyname = data[i : i + size].decode("utf8")
        i += size

        return cls(object_id, timestamp, proxyname), i

    def __str__(self) -> str:
        text = f"{self.__class__.__name__}("
        text += f"object_id={self.object_id}, "
        text += f"timestamp={self.timestamp}, "
        text += f"proxyname={self.proxyname}"
        text += ")"

        return text


class RequestData:
    __slots__ = ["http_version", "method", "url", "headers", "content", "trailers", "meta", "session"]

    def __init__(
        self,
        http_version: bytes,
        method: bytes,
        url: bytes,
        headers: bytes,
        content: bytes,
        trailers: bytes,
        meta: SnifferMetadata,
        session: Optional[int] = None,
    ):
        self.http_version = http_version
        self.method = method
        self.url = url
        self.headers = headers
        self.content = content
        self.trailers = trailers
        self.meta = meta
        self.session = session

    def to_bytes(self) -> bytes:
        data = b""
        data += SnifferMessageType.REQUEST_DATA.to_bytes(8, "big")
        data += bytes_to_varlen_bytes(self.http_version)
        data += bytes_to_varlen_bytes(self.method)
        data += bytes_to_varlen_bytes(self.url)
        data += bytes_to_varlen_bytes(self.headers)
        data += bytes_to_varlen_bytes(self.content)
        data += bytes_to_varlen_bytes(self.trailers)
        data += self.meta.to_bytes()
        data += SnifferInt64.to_bytes(self.session)

        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> tuple[RequestData, int]:
        i = 0
        message_type = int.from_bytes(data[i : i + 8], "big")
        i += 8
        assert message_type == SnifferMessageType.REQUEST_DATA

        components = []
        for _ in range(6):
            size = int.from_bytes(data[i : i + 8], "big")
            i += 8
            obj = data[i : i + size]
            i += size
            components.append(obj)

        http_version = components[0]
        method = components[1]
        url = components[2]
        headers = components[3]
        content = components[4]
        trailers = components[5]

        meta, used = SnifferMetadata.from_bytes(data[i:])
        i += used

        session, used = sniffer_data_from_bytes(data[i:])
        assert isinstance(session, int) or session is None
        i += used

        return cls(http_version, method, url, headers, content, trailers, meta, session), i

    def __str__(self) -> str:
        text = f"{self.__class__.__name__}("
        text += f"http_version={self.http_version!r}, "
        text += f"method={self.method!r}, "
        text += f"url={self.url!r}, "
        text += f"headers={self.headers!r}, "
        text += f"content={self.content!r}, "
        text += f"trailers={self.trailers!r}, "
        text += f"meta={self.meta},"
        text += f"session={self.session}"
        text += ")"

        return text

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RequestData):
            raise NotImplementedError

        return (
            self.http_version == other.http_version
            and self.method == other.method
            and self.url == other.url
            and self.headers == other.headers
            and self.content == other.content
            and self.trailers == other.trailers
        )


class ResponseData:
    __slots__ = ["http_version", "status_code", "reason", "headers", "content", "trailers", "meta", "session"]

    def __init__(
        self,
        http_version: bytes,
        status_code: int,
        reason: bytes,
        headers: bytes,
        content: bytes,
        trailers: bytes,
        meta: SnifferMetadata,
        session: Optional[int] = None,
    ):
        self.http_version = http_version
        self.status_code = status_code
        self.reason = reason
        self.headers = headers
        self.content = content
        self.trailers = trailers
        self.meta = meta
        self.session = session

    def to_bytes(self) -> bytes:
        data = b""
        data += SnifferMessageType.RESPONSE_DATA.to_bytes(8, "big")
        data += bytes_to_varlen_bytes(self.http_version)
        data += self.status_code.to_bytes(8, "big")
        data += bytes_to_varlen_bytes(self.reason)
        data += bytes_to_varlen_bytes(self.headers)
        data += bytes_to_varlen_bytes(self.content)
        data += bytes_to_varlen_bytes(self.trailers)
        data += self.meta.to_bytes()
        data += SnifferInt64.to_bytes(self.session)

        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> tuple[ResponseData, int]:
        i = 0
        message_type = int.from_bytes(data[i : i + 8], "big")
        i += 8
        assert message_type == SnifferMessageType.RESPONSE_DATA

        size = int.from_bytes(data[i : i + 8], "big")
        i += 8
        http_version = data[i : i + size]
        i += size

        status_code = int.from_bytes(data[i : i + 8], "big")
        i += 8

        components = []
        for _ in range(4):
            size = int.from_bytes(data[i : i + 8], "big")
            i += 8
            obj = data[i : i + size]
            i += size
            components.append(obj)

        reason = components[0]
        headers = components[1]
        content = components[2]
        trailers = components[3]

        meta, used = SnifferMetadata.from_bytes(data[i:])
        i += used

        session, used = sniffer_data_from_bytes(data[i:])
        assert isinstance(session, int) or session is None
        i += used

        return cls(http_version, status_code, reason, headers, content, trailers, meta, session), i

    def __str__(self) -> str:
        text = f"{self.__class__.__name__}("
        text += f"http_version={self.http_version!r}, "
        text += f"status_code={self.status_code}, "
        text += f"reasom={self.reason!r}, "
        text += f"headers={self.headers!r}, "
        text += f"content={self.content!r}, "
        text += f"trailers={self.trailers!r}, "
        text += f"meta={self.meta},"
        text += f"session={self.session}"
        text += ")"

        return text

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResponseData):
            raise NotImplementedError

        return (
            self.http_version == other.http_version
            and self.status_code == other.status_code
            and self.reason == other.reason
            and self.headers == other.headers
            and self.content == other.content
            and self.trailers == other.trailers
        )


class ProxyEvent:
    CONNECT = 1
    CLOSE = 2

    def __init__(self, event: int):
        self.event = event
        self.session: Optional[int] = None

    @classmethod
    def from_bytes(cls, data: bytes) -> tuple[ProxyEvent, int]:
        i = 0
        message_type = int.from_bytes(data[i : i + 8], "big")
        i += 8
        assert message_type == SnifferMessageType.PROXY_EVENT

        event = int.from_bytes(data[i : i + 8], "big")
        i += 8

        return cls(event), i

    def to_bytes(self) -> bytes:
        data = b""
        data += SnifferMessageType.PROXY_EVENT.to_bytes(8, "big")
        data += self.event.to_bytes(8, "big")

        return data


class SnifferError:
    def __init__(self, error_msg: str, error_type: str, session: Optional[int] = None):
        self.error_msg = error_msg
        self.error_type = error_type
        self.session = session

    def to_bytes(self) -> bytes:
        data = b""
        data += SnifferMessageType.SNIFFER_ERROR.to_bytes(8, "big")
        data += SnifferString.to_bytes(self.error_msg)
        data += SnifferString.to_bytes(self.error_type)
        data += SnifferInt64.to_bytes(self.session)

        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> tuple[SnifferError, int]:
        i = 0
        message_type = int.from_bytes(data[i : i + 8], "big")
        i += 8
        assert message_type == SnifferMessageType.SNIFFER_ERROR

        error_msg, used = SnifferString.from_bytes(data[i:])
        i += used

        error_type, used = SnifferString.from_bytes(data[i:])
        i += used

        session = int.from_bytes(data[i : i + 8], "big")
        i += 8

        return cls(error_msg, error_type, session), i


class SniffCommand:
    NOP = 1
    REPLACE = 2
    CANCEL = 3
    CLOSE_CLIENT = 4

    __slots__ = ["command", "request", "response", "meta", "session"]

    def __init__(
        self,
        command: int,
        request: Optional[RequestData] = None,
        response: Optional[ResponseData] = None,
        meta: Optional[SnifferMetadata] = None,
        session: Optional[int] = None,
    ):
        self.command = command
        self.request = request
        self.response = response
        self.meta = meta
        self.session = session

    def to_bytes(self) -> bytes:
        data = b""
        data += SnifferMessageType.SNIFF_COMMAND.to_bytes(8, "big")
        data += self.command.to_bytes(8, "big")
        data += self.request.to_bytes() if self.request is not None else SnifferNone.to_bytes()
        data += self.response.to_bytes() if self.response is not None else SnifferNone.to_bytes()
        data += self.meta.to_bytes() if self.meta is not None else SnifferNone.to_bytes()
        data += SnifferInt64.to_bytes(self.session) if self.session is not None else SnifferNone.to_bytes()

        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> tuple[SniffCommand, int]:
        i = 0

        message_type = int.from_bytes(data[i : i + 8], "big")
        i += 8
        assert message_type == SnifferMessageType.SNIFF_COMMAND

        command = int.from_bytes(data[i : i + 8], "big")
        i += 8

        request, used = sniffer_data_from_bytes(data[i:])
        i += used
        assert isinstance(request, RequestData) or request is None

        response, used = sniffer_data_from_bytes(data[i:])
        i += used
        assert isinstance(response, ResponseData) or response is None

        meta, used = sniffer_data_from_bytes(data[i:])
        i += used
        assert isinstance(meta, SnifferMetadata) or meta is None

        session, used = sniffer_data_from_bytes(data[i:])
        assert isinstance(session, int) or session is None
        i += used

        return cls(command, request, response, meta, session), i


class ProxyException(Exception):
    def __init__(self, obj: Optional[SnifferError], *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.obj = obj


class SnifferClientException(Exception):
    def __init__(self, obj: Optional[SnifferMessage], *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.obj = obj


SnifferMessage: TypeAlias = Union[SniffCommand, SnifferError]
ProxyMessage: TypeAlias = Union[RequestData, ResponseData, ProxyEvent, SnifferError]
SkopoMessage: TypeAlias = Union[ProxyMessage, SnifferError]


def sniffer_data_from_bytes(data: bytes) -> tuple[Union[RequestData, ResponseData, ProxyEvent, SniffCommand, int, str, None], int]:
    message_type = int.from_bytes(data[:8], "big")
    if message_type == SnifferMessageType.REQUEST_DATA:
        return RequestData.from_bytes(data)
    elif message_type == SnifferMessageType.RESPONSE_DATA:
        return ResponseData.from_bytes(data)
    elif message_type == SnifferMessageType.PROXY_EVENT:
        return ProxyEvent.from_bytes(data)
    elif message_type == SnifferMessageType.SNIFF_COMMAND:
        return SniffCommand.from_bytes(data)
    elif message_type == SnifferMessageType.INT64:
        assert len(data) >= 16, "Not enough bytes to decode"
        return int.from_bytes(data[8:16], "big"), 16
    elif message_type == SnifferMessageType.STRING:
        return SnifferString.from_bytes(data)
    elif message_type == SnifferMessageType.NONE:
        return None, 8
    else:
        raise ProxyException(None, f"Unknown message type: {message_type}")


class SnifferProxyClient:
    def __init__(self) -> None:
        self.session_to_messages: dict[Optional[int], list[SnifferMessage]] = defaultdict(list)

    def _get_data(self) -> bytes:
        raise NotImplementedError

    def pushback_message(self, obj: SnifferMessage) -> None:
        self.session_to_messages[obj.session].append(obj)

    def get_message(self, ignore_error: bool = False, session: Optional[int] = None) -> SnifferMessage:
        while len(self.session_to_messages[session]):
            queue_obj = self.session_to_messages[session].pop(0)

            if isinstance(queue_obj, SnifferError) and not ignore_error:
                raise ProxyException(queue_obj)

            if isinstance(queue_obj, SniffCommand):
                if queue_obj.session is None and session is not None:
                    raise SnifferClientException(queue_obj, "Received sessionless message in a context with session")
                return queue_obj

        del self.session_to_messages[session]

        while True:
            data = self._get_data()
            obj, _ = sniffer_data_from_bytes(data)

            if isinstance(obj, SnifferError) and not ignore_error:
                raise ProxyException(obj)

            if isinstance(obj, SniffCommand):
                if obj.session != session:
                    self.pushback_message(obj)
                else:
                    return obj

    def get_command(self, ignore_error: bool = False, session: Optional[int] = None) -> SniffCommand:
        while True:
            msg = self.get_message(ignore_error, session)
            if not isinstance(msg, SniffCommand):
                raise ProxyException(msg, "Expected message of type SniffCommand")
            return msg

    def _send_data(self, data: bytes) -> None:
        raise NotImplementedError

    def send_proxy_message(self, obj: ProxyMessage, session: Optional[int] = None) -> None:
        if hasattr(obj, "session"):
            obj.session = session
        data = obj.to_bytes()
        self._send_data(data)

    def send_request_data(self, obj: RequestData, session: Optional[int] = None) -> None:
        self.send_proxy_message(obj, session)

    def send_response_data(self, obj: ResponseData, session: Optional[int] = None) -> None:
        self.send_proxy_message(obj, session)

    def send_proxy_event(self, obj: ProxyEvent, session: Optional[int] = None) -> None:
        self.send_proxy_message(obj, session)

    def send_error(self, msg: SnifferError, session: Optional[int] = None) -> None:
        msg.session = session
        data = msg.to_bytes()
        self._send_data(data)

    def new_session(self) -> SnifferClientSession:
        return SnifferClientSession(self)


class SnifferClientSession:
    _LAST_ID = 1

    def __init__(self, client: SnifferProxyClient) -> None:
        self.client = client
        self.id = SnifferClientSession._LAST_ID
        SnifferClientSession._LAST_ID += 1

    def __getattr__(self, key: str) -> object:
        value = getattr(self.client, key)
        if callable(value):
            value = functools.partial(value, session=self.id)

        return value


def to_sock_datagram(data: bytes) -> bytes:
    size = len(data)
    return size.to_bytes(8, "big") + data


async def async_read_sock_datagram(reader: StreamReader) -> bytes:
    data_size = await reader.readexactly(8)
    size = int.from_bytes(data_size, "big")
    data = await reader.readexactly(size)
    return data


def read_sock_datagram(sock: socket.socket) -> bytes:
    data_size = sock.recv(8)
    if len(data_size) != 8:
        raise ProxyException("Received less than expected data")
    size = int.from_bytes(data_size, "big")
    data = sock.recv(size)
    if len(data) != size:
        raise ProxyException("Received less than expected data")
    return data
