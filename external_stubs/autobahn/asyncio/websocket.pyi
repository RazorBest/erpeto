import asyncio
from _typeshed import Incomplete
from autobahn.wamp import websocket
from autobahn.websocket import protocol
from typing import Optional

__all__ = ['WebSocketServerProtocol', 'WebSocketClientProtocol', 'WebSocketServerFactory', 'WebSocketClientFactory', 'WampWebSocketServerProtocol', 'WampWebSocketClientProtocol', 'WampWebSocketServerFactory', 'WampWebSocketClientFactory']

class WebSocketAdapterProtocol(asyncio.Protocol):
    log: Incomplete
    peer: Optional[str]
    is_server: Optional[bool]
    transport: Incomplete
    receive_queue: Incomplete
    def connection_made(self, transport) -> None: ...
    def connection_lost(self, exc) -> None: ...
    def data_received(self, data) -> None: ...
    def registerProducer(self, producer, streaming) -> None: ...
    def unregisterProducer(self) -> None: ...

class WebSocketServerProtocol(WebSocketAdapterProtocol, protocol.WebSocketServerProtocol):
    log: Incomplete

class WebSocketClientProtocol(WebSocketAdapterProtocol, protocol.WebSocketClientProtocol):
    log: Incomplete
    def startTLS(self) -> None: ...

class WebSocketAdapterFactory:
    log: Incomplete
    def __call__(self): ...

class WebSocketServerFactory(WebSocketAdapterFactory, protocol.WebSocketServerFactory):
    log: Incomplete
    protocol = WebSocketServerProtocol
    loop: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...

class WebSocketClientFactory(WebSocketAdapterFactory, protocol.WebSocketClientFactory):
    log: Incomplete
    loop: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...

class WampWebSocketServerProtocol(websocket.WampWebSocketServerProtocol, WebSocketServerProtocol):
    log: Incomplete

class WampWebSocketServerFactory(websocket.WampWebSocketServerFactory, WebSocketServerFactory):
    log: Incomplete
    protocol = WampWebSocketServerProtocol
    def __init__(self, factory, *args, **kwargs) -> None: ...

class WampWebSocketClientProtocol(websocket.WampWebSocketClientProtocol, WebSocketClientProtocol):
    log: Incomplete

class WampWebSocketClientFactory(websocket.WampWebSocketClientFactory, WebSocketClientFactory):
    log: Incomplete
    protocol = WampWebSocketClientProtocol
    def __init__(self, factory, *args, **kwargs) -> None: ...
