from _typeshed import Incomplete

__all__ = ['ConnectionRequest', 'ConnectingRequest', 'ConnectionResponse', 'ConnectionAccept', 'ConnectionDeny', 'Message', 'IncomingMessage', 'OutgoingMessage', 'Ping']

class ConnectionRequest:
    peer: Incomplete
    headers: Incomplete
    host: Incomplete
    path: Incomplete
    params: Incomplete
    version: Incomplete
    origin: Incomplete
    protocols: Incomplete
    extensions: Incomplete
    def __init__(self, peer, headers, host, path, params, version, origin, protocols, extensions) -> None: ...
    def __json__(self): ...

class ConnectingRequest:
    host: Incomplete
    port: Incomplete
    resource: Incomplete
    headers: Incomplete
    useragent: Incomplete
    origin: Incomplete
    protocols: Incomplete
    def __init__(self, host: Incomplete | None = None, port: Incomplete | None = None, resource: Incomplete | None = None, headers: Incomplete | None = None, useragent: Incomplete | None = None, origin: Incomplete | None = None, protocols: Incomplete | None = None) -> None: ...
    def __json__(self): ...

class ConnectionResponse:
    peer: Incomplete
    headers: Incomplete
    version: Incomplete
    protocol: Incomplete
    extensions: Incomplete
    def __init__(self, peer, headers, version, protocol, extensions) -> None: ...
    def __json__(self): ...

class ConnectionAccept:
    subprotocol: Incomplete
    headers: Incomplete
    def __init__(self, subprotocol: Incomplete | None = None, headers: Incomplete | None = None) -> None: ...

class ConnectionDeny(Exception):
    BAD_REQUEST: int
    FORBIDDEN: int
    NOT_FOUND: int
    NOT_ACCEPTABLE: int
    REQUEST_TIMEOUT: int
    INTERNAL_SERVER_ERROR: int
    NOT_IMPLEMENTED: int
    SERVICE_UNAVAILABLE: int
    code: Incomplete
    reason: Incomplete
    def __init__(self, code, reason: Incomplete | None = None) -> None: ...

class Message: ...

class IncomingMessage(Message):
    payload: Incomplete
    is_binary: Incomplete
    def __init__(self, payload, is_binary: bool = False) -> None: ...

class OutgoingMessage(Message):
    payload: Incomplete
    is_binary: Incomplete
    skip_compress: Incomplete
    def __init__(self, payload, is_binary: bool = False, skip_compress: bool = False) -> None: ...

class Ping:
    payload: Incomplete
    def __init__(self, payload: Incomplete | None = None) -> None: ...
