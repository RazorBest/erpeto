import abc
from _typeshed import Incomplete
from autobahn.wamp.types import TransportDetails
from autobahn.websocket.types import ConnectingRequest, ConnectionRequest, ConnectionResponse
from typing import Dict, Optional, Tuple, Union

__all__ = ['IWebSocketServerChannelFactory', 'IWebSocketClientChannelFactory', 'IWebSocketChannel', 'IWebSocketChannelFrameApi', 'IWebSocketChannelStreamingApi']

class IWebSocketClientAgent(abc.ABC):
    def open(self, transport_config, options, protocol_class: Incomplete | None = None) -> None: ...

class IWebSocketServerChannelFactory(abc.ABC, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, url: Incomplete | None = None, protocols: Incomplete | None = None, server: Incomplete | None = None, headers: Incomplete | None = None, externalPort: Incomplete | None = None): ...
    @abc.abstractmethod
    def setSessionParameters(self, url: Incomplete | None = None, protocols: Incomplete | None = None, server: Incomplete | None = None, headers: Incomplete | None = None, externalPort: Incomplete | None = None): ...
    @abc.abstractmethod
    def setProtocolOptions(self, versions: Incomplete | None = None, webStatus: Incomplete | None = None, utf8validateIncoming: Incomplete | None = None, maskServerFrames: Incomplete | None = None, requireMaskedClientFrames: Incomplete | None = None, applyMask: Incomplete | None = None, maxFramePayloadSize: Incomplete | None = None, maxMessagePayloadSize: Incomplete | None = None, autoFragmentSize: Incomplete | None = None, failByDrop: Incomplete | None = None, echoCloseCodeReason: Incomplete | None = None, openHandshakeTimeout: Incomplete | None = None, closeHandshakeTimeout: Incomplete | None = None, tcpNoDelay: Incomplete | None = None, perMessageCompressionAccept: Incomplete | None = None, autoPingInterval: Incomplete | None = None, autoPingTimeout: Incomplete | None = None, autoPingSize: Incomplete | None = None, serveFlashSocketPolicy: Incomplete | None = None, flashSocketPolicy: Incomplete | None = None, allowedOrigins: Incomplete | None = None, allowNullOrigin: bool = False, maxConnections: Incomplete | None = None, trustXForwardedFor: int = 0): ...
    @abc.abstractmethod
    def resetProtocolOptions(self): ...

class IWebSocketClientChannelFactory(abc.ABC, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, url: Incomplete | None = None, origin: Incomplete | None = None, protocols: Incomplete | None = None, useragent: Incomplete | None = None, headers: Incomplete | None = None, proxy: Incomplete | None = None): ...
    @abc.abstractmethod
    def setSessionParameters(self, url: Incomplete | None = None, origin: Incomplete | None = None, protocols: Incomplete | None = None, useragent: Incomplete | None = None, headers: Incomplete | None = None, proxy: Incomplete | None = None): ...
    @abc.abstractmethod
    def setProtocolOptions(self, version: Incomplete | None = None, utf8validateIncoming: Incomplete | None = None, acceptMaskedServerFrames: Incomplete | None = None, maskClientFrames: Incomplete | None = None, applyMask: Incomplete | None = None, maxFramePayloadSize: Incomplete | None = None, maxMessagePayloadSize: Incomplete | None = None, autoFragmentSize: Incomplete | None = None, failByDrop: Incomplete | None = None, echoCloseCodeReason: Incomplete | None = None, serverConnectionDropTimeout: Incomplete | None = None, openHandshakeTimeout: Incomplete | None = None, closeHandshakeTimeout: Incomplete | None = None, tcpNoDelay: Incomplete | None = None, perMessageCompressionOffers: Incomplete | None = None, perMessageCompressionAccept: Incomplete | None = None, autoPingInterval: Incomplete | None = None, autoPingTimeout: Incomplete | None = None, autoPingSize: Incomplete | None = None): ...
    @abc.abstractmethod
    def resetProtocolOptions(self): ...

class IWebSocketChannel(abc.ABC, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def onConnecting(self, transport_details: TransportDetails) -> Optional[ConnectingRequest]: ...
    @abc.abstractmethod
    def onConnect(self, request_or_response: Union[ConnectionRequest, ConnectionResponse]) -> Union[Optional[str], Tuple[Optional[str], Dict[str, str]]]: ...
    @abc.abstractmethod
    def onOpen(self): ...
    @abc.abstractmethod
    def sendMessage(self, payload: bytes, isBinary: bool): ...
    @abc.abstractmethod
    def onMessage(self, payload: bytes, isBinary: bool): ...
    @abc.abstractmethod
    def sendClose(self, code: Optional[int] = None, reason: Optional[str] = None): ...
    @abc.abstractmethod
    def onClose(self, wasClean: bool, code: int, reason: str): ...
    @abc.abstractmethod
    def sendPing(self, payload: Optional[bytes] = None): ...
    @abc.abstractmethod
    def onPing(self, payload: bytes): ...
    @abc.abstractmethod
    def sendPong(self, payload: Optional[bytes] = None): ...
    @abc.abstractmethod
    def onPong(self, payload: bytes): ...

class IWebSocketChannelFrameApi(IWebSocketChannel, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def onMessageBegin(self, isBinary: bool): ...
    @abc.abstractmethod
    def onMessageFrame(self, payload: bytes): ...
    @abc.abstractmethod
    def onMessageEnd(self): ...
    @abc.abstractmethod
    def beginMessage(self, isBinary: bool = False, doNotCompress: bool = False): ...
    @abc.abstractmethod
    def sendMessageFrame(self, payload: bytes, sync: bool = False): ...
    @abc.abstractmethod
    def endMessage(self): ...

class IWebSocketChannelStreamingApi(IWebSocketChannelFrameApi, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def onMessageFrameBegin(self, length: int): ...
    @abc.abstractmethod
    def onMessageFrameData(self, payload: bytes): ...
    @abc.abstractmethod
    def onMessageFrameEnd(self): ...
    @abc.abstractmethod
    def beginMessageFrame(self, length: int): ...
    @abc.abstractmethod
    def sendMessageFrameData(self, payload: bytes, sync: bool = False): ...