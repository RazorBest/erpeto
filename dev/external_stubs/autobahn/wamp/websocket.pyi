from _typeshed import Incomplete
from autobahn.wamp.types import TransportDetails
from autobahn.websocket.types import ConnectionRequest, ConnectionResponse
from typing import Dict, Optional, Tuple

__all__ = ['WampWebSocketServerProtocol', 'WampWebSocketClientProtocol', 'WampWebSocketServerFactory', 'WampWebSocketClientFactory']

class WampWebSocketProtocol:
    def onOpen(self) -> None: ...
    def onClose(self, wasClean: bool, code: int, reason: Optional[str]): ...
    def onMessage(self, payload: bytes, isBinary: bool): ...
    def send(self, msg) -> None: ...
    def isOpen(self): ...
    @property
    def transport_details(self) -> Optional[TransportDetails]: ...
    def close(self) -> None: ...
    def abort(self) -> None: ...

class WampWebSocketServerProtocol(WampWebSocketProtocol):
    STRICT_PROTOCOL_NEGOTIATION: bool
    def onConnect(self, request: ConnectionRequest) -> Tuple[Optional[str], Dict[str, str]]: ...

class WampWebSocketClientProtocol(WampWebSocketProtocol):
    STRICT_PROTOCOL_NEGOTIATION: bool
    def onConnect(self, response: ConnectionResponse): ...

class WampWebSocketFactory:
    def __init__(self, factory, serializers: Incomplete | None = None) -> None: ...

class WampWebSocketServerFactory(WampWebSocketFactory): ...
class WampWebSocketClientFactory(WampWebSocketFactory): ...
