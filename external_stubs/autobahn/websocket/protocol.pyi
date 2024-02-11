import twisted.internet.protocol

from _typeshed import Incomplete
from autobahn.util import ObservableMixin
from autobahn.wamp.types import TransportDetails
from autobahn.websocket.types import ConnectingRequest, ConnectionRequest, ConnectionResponse
from typing import Callable, Dict, Optional, Tuple, Union

__all__ = ['WebSocketProtocol', 'WebSocketFactory', 'WebSocketServerProtocol', 'WebSocketServerFactory', 'WebSocketClientProtocol', 'WebSocketClientFactory']

class TrafficStats:
    def __init__(self) -> None: ...
    outgoingOctetsWireLevel: int
    outgoingOctetsWebSocketLevel: int
    outgoingOctetsAppLevel: int
    outgoingWebSocketFrames: int
    outgoingWebSocketMessages: int
    incomingOctetsWireLevel: int
    incomingOctetsWebSocketLevel: int
    incomingOctetsAppLevel: int
    incomingWebSocketFrames: int
    incomingWebSocketMessages: int
    preopenOutgoingOctetsWireLevel: int
    preopenIncomingOctetsWireLevel: int
    def reset(self) -> None: ...
    def __json__(self): ...

class FrameHeader:
    opcode: Incomplete
    fin: Incomplete
    rsv: Incomplete
    length: Incomplete
    mask: Incomplete
    def __init__(self, opcode, fin, rsv, length, mask) -> None: ...

class Timings:
    def __init__(self) -> None: ...
    def track(self, key) -> None: ...
    def diff(self, startKey, endKey, formatted: bool = True): ...
    def __getitem__(self, key): ...
    def __iter__(self): ...

class WebSocketProtocol(ObservableMixin):
    peer: Optional[str]
    SUPPORTED_SPEC_VERSIONS: Incomplete
    SUPPORTED_PROTOCOL_VERSIONS: Incomplete
    SPEC_TO_PROTOCOL_VERSION: Incomplete
    PROTOCOL_TO_SPEC_VERSION: Incomplete
    DEFAULT_SPEC_VERSION: int
    MESSAGE_TYPE_TEXT: int
    MESSAGE_TYPE_BINARY: int
    STATE_CLOSED: int
    STATE_CONNECTING: int
    STATE_CLOSING: int
    STATE_OPEN: int
    STATE_PROXY_CONNECTING: int
    SEND_STATE_GROUND: int
    SEND_STATE_MESSAGE_BEGIN: int
    SEND_STATE_INSIDE_MESSAGE: int
    SEND_STATE_INSIDE_MESSAGE_FRAME: int
    CLOSE_STATUS_CODE_NORMAL: int
    CLOSE_STATUS_CODE_GOING_AWAY: int
    CLOSE_STATUS_CODE_PROTOCOL_ERROR: int
    CLOSE_STATUS_CODE_UNSUPPORTED_DATA: int
    CLOSE_STATUS_CODE_RESERVED1: int
    CLOSE_STATUS_CODE_NULL: int
    CLOSE_STATUS_CODE_ABNORMAL_CLOSE: int
    CLOSE_STATUS_CODE_INVALID_PAYLOAD: int
    CLOSE_STATUS_CODE_POLICY_VIOLATION: int
    CLOSE_STATUS_CODE_MESSAGE_TOO_BIG: int
    CLOSE_STATUS_CODE_MANDATORY_EXTENSION: int
    CLOSE_STATUS_CODE_INTERNAL_ERROR: int
    CLOSE_STATUS_CODE_SERVICE_RESTART: int
    CLOSE_STATUS_CODE_TRY_AGAIN_LATER: int
    CLOSE_STATUS_CODE_UNASSIGNED1: int
    CLOSE_STATUS_CODE_TLS_HANDSHAKE_FAILED: int
    CLOSE_STATUS_CODES_ALLOWED: Incomplete
    CONFIG_ATTRS_COMMON: Incomplete
    CONFIG_ATTRS_SERVER: Incomplete
    CONFIG_ATTRS_CLIENT: Incomplete
    is_closed: Incomplete
    is_open: Incomplete
    def __init__(self) -> None: ...
    @property
    def transport_details(self) -> Optional[TransportDetails]: ...
    def onOpen(self) -> None: ...
    message_is_binary: Incomplete
    message_data: Incomplete
    message_data_total_length: int
    def onMessageBegin(self, isBinary) -> None: ...
    frame_length: Incomplete
    frame_data: Incomplete
    wasMaxMessagePayloadSizeExceeded: bool
    wasMaxFramePayloadSizeExceeded: bool
    def onMessageFrameBegin(self, length) -> None: ...
    def onMessageFrameData(self, payload) -> None: ...
    def onMessageFrameEnd(self) -> None: ...
    def onMessageFrame(self, payload) -> None: ...
    def onMessageEnd(self) -> None: ...
    def onMessage(self, payload, isBinary) -> None: ...
    def onPing(self, payload) -> None: ...
    def onPong(self, payload) -> None: ...
    def onClose(self, wasClean, code, reason) -> None: ...
    remoteCloseCode: Incomplete
    remoteCloseReason: Incomplete
    closeHandshakeTimeoutCall: Incomplete
    wasClean: bool
    serverConnectionDropTimeoutCall: Incomplete
    def onCloseFrame(self, code, reasonRaw): ...
    wasNotCleanReason: str
    wasServerConnectionDropTimeout: bool
    def onServerConnectionDropTimeout(self) -> None: ...
    openHandshakeTimeoutCall: Incomplete
    wasOpenHandshakeTimeout: bool
    def onOpenHandshakeTimeout(self) -> None: ...
    wasCloseHandshakeTimeout: bool
    def onCloseHandshakeTimeout(self) -> None: ...
    def onAutoPong(self, ping_sent, ping_seq, pong_received, pong_rtt, payload) -> None: ...
    autoPingTimeoutCall: Incomplete
    def onAutoPingTimeout(self) -> None: ...
    droppedByMe: bool
    state: Incomplete
    def dropConnection(self, abort: bool = False) -> None: ...
    trackTimings: Incomplete
    trackedTimings: Incomplete
    def setTrackTimings(self, enable) -> None: ...
    def logRxOctets(self, data) -> None: ...
    def logTxOctets(self, data, sync) -> None: ...
    def logRxFrame(self, frameHeader, payload) -> None: ...
    def logTxFrame(self, frameHeader, payload, repeatLength, chopsize, sync) -> None: ...
    def consumeData(self) -> None: ...
    def processProxyConnect(self) -> None: ...
    def processHandshake(self) -> None: ...
    def sendData(self, data, sync: bool = False, chopsize: Incomplete | None = None) -> None: ...
    def sendPreparedMessage(self, preparedMsg) -> None: ...
    current_frame_masker: Incomplete
    data: Incomplete
    current_frame: Incomplete
    def processData(self): ...
    control_frame_data: Incomplete
    inside_message: bool
    utf8validateIncomingCurrentMessage: bool
    utf8validateLast: Incomplete
    def onFrameBegin(self) -> None: ...
    def onFrameData(self, payload): ...
    def onFrameEnd(self): ...
    autoPingPending: Incomplete
    autoPingPendingSent: Incomplete
    autoPingPendingCall: Incomplete
    def processControlFrame(self): ...
    def sendFrame(self, opcode, payload: bytes = b'', fin: bool = True, rsv: int = 0, mask: Incomplete | None = None, payload_len: Incomplete | None = None, chopsize: Incomplete | None = None, sync: bool = False) -> None: ...
    def sendPing(self, payload: Incomplete | None = None) -> None: ...
    def sendPong(self, payload: Incomplete | None = None) -> None: ...
    closedByMe: Incomplete
    localCloseCode: Incomplete
    localCloseReason: Incomplete
    def sendCloseFrame(self, code: Incomplete | None = None, reasonUtf8: Incomplete | None = None, isReply: bool = False) -> None: ...
    def sendClose(self, code: Incomplete | None = None, reason: Incomplete | None = None) -> None: ...
    send_message_opcode: Incomplete
    send_state: Incomplete
    send_compressed: bool
    def beginMessage(self, isBinary: bool = False, doNotCompress: bool = False) -> None: ...
    send_message_frame_length: Incomplete
    send_message_frame_mask: Incomplete
    send_message_frame_masker: Incomplete
    def beginMessageFrame(self, length) -> None: ...
    def sendMessageFrameData(self, payload, sync: bool = False): ...
    def endMessage(self) -> None: ...
    def sendMessageFrame(self, payload, sync: bool = False) -> None: ...
    def sendMessage(self, payload, isBinary: bool = False, fragmentSize: Incomplete | None = None, sync: bool = False, doNotCompress: bool = False) -> None: ...

class PreparedMessage:
    payload: Incomplete
    binary: Incomplete
    doNotCompress: Incomplete
    payloadHybi: Incomplete
    def __init__(self, payload, isBinary, applyMask, doNotCompress) -> None: ...

class WebSocketFactory:
    def prepareMessage(self, payload, isBinary: bool = False, doNotCompress: bool = False): ...

class WebSocketServerProtocol(WebSocketProtocol):
    CONFIG_ATTRS: Incomplete
    def onConnect(self, request: ConnectionRequest) -> Union[Optional[str], Tuple[Optional[str], Dict[str, str]]]: ...
    def processProxyConnect(self) -> None: ...
    http_request_data: Incomplete
    peer: Incomplete
    http_request_uri: Incomplete
    http_request_path: Incomplete
    http_request_params: Incomplete
    http_request_host: Incomplete
    websocket_version: Incomplete
    websocket_protocols: Incomplete
    websocket_origin: str
    websocket_extensions: Incomplete
    data: Incomplete
    wasServingFlashSocketPolicyFile: bool
    def processHandshake(self): ...
    websocket_protocol_in_use: Incomplete
    websocket_extensions_in_use: Incomplete
    http_response_data: Incomplete
    state: Incomplete
    openHandshakeTimeoutCall: Incomplete
    inside_message: bool
    current_frame: Incomplete
    autoPingPendingCall: Incomplete
    def succeedHandshake(self, res): ...
    wasNotCleanReason: Incomplete
    def failHandshake(self, reason, code: int = 400, responseHeaders: Incomplete | None = None) -> None: ...
    def sendHttpErrorResponse(self, code, reason, responseHeaders: Incomplete | None = None) -> None: ...
    def sendHtml(self, html) -> None: ...
    def sendRedirect(self, url) -> None: ...
    def sendServerStatus(self, redirectUrl: Incomplete | None = None, redirectAfter: int = 0) -> None: ...

class WebSocketServerFactory(WebSocketFactory):
    protocol: Optional[Callable[[], twisted.internet.protocol.Protocol]]
    isServer: bool
    logOctets: bool
    logFrames: bool
    trackTimings: bool
    countConnections: int
    def __init__(self, url: Incomplete | None = None, protocols: Incomplete | None = None, server=..., headers: Incomplete | None = None, externalPort: Incomplete | None = None) -> None: ...
    url: Incomplete
    isSecure: Incomplete
    host: Incomplete
    port: Incomplete
    resource: Incomplete
    path: Incomplete
    params: Incomplete
    protocols: Incomplete
    server: Incomplete
    headers: Incomplete
    externalPort: Incomplete
    def setSessionParameters(self, url: Incomplete | None = None, protocols: Incomplete | None = None, server: Incomplete | None = None, headers: Incomplete | None = None, externalPort: Incomplete | None = None) -> None: ...
    versions: Incomplete
    webStatus: bool
    utf8validateIncoming: bool
    requireMaskedClientFrames: bool
    maskServerFrames: bool
    applyMask: bool
    maxFramePayloadSize: int
    maxMessagePayloadSize: int
    autoFragmentSize: int
    failByDrop: bool
    echoCloseCodeReason: bool
    openHandshakeTimeout: int
    closeHandshakeTimeout: int
    tcpNoDelay: bool
    serveFlashSocketPolicy: bool
    flashSocketPolicy: str
    perMessageCompressionAccept: Incomplete
    autoPingInterval: int
    autoPingTimeout: int
    autoPingSize: int
    autoPingRestartOnAnyTraffic: bool
    allowedOrigins: Incomplete
    allowedOriginsPatterns: Incomplete
    allowNullOrigin: bool
    maxConnections: int
    trustXForwardedFor: int
    def resetProtocolOptions(self) -> None: ...
    def setProtocolOptions(self, versions: Incomplete | None = None, webStatus: Incomplete | None = None, utf8validateIncoming: Incomplete | None = None, maskServerFrames: Incomplete | None = None, requireMaskedClientFrames: Incomplete | None = None, applyMask: Incomplete | None = None, maxFramePayloadSize: Incomplete | None = None, maxMessagePayloadSize: Incomplete | None = None, autoFragmentSize: Incomplete | None = None, failByDrop: Incomplete | None = None, echoCloseCodeReason: Incomplete | None = None, openHandshakeTimeout: Incomplete | None = None, closeHandshakeTimeout: Incomplete | None = None, tcpNoDelay: Incomplete | None = None, perMessageCompressionAccept: Incomplete | None = None, autoPingInterval: Incomplete | None = None, autoPingTimeout: Incomplete | None = None, autoPingSize: Incomplete | None = None, autoPingRestartOnAnyTraffic: Incomplete | None = None, serveFlashSocketPolicy: Incomplete | None = None, flashSocketPolicy: Incomplete | None = None, allowedOrigins: Incomplete | None = None, allowNullOrigin: bool = False, maxConnections: Incomplete | None = None, trustXForwardedFor: Incomplete | None = None) -> None: ...
    def getConnectionCount(self): ...

class WebSocketClientProtocol(WebSocketProtocol):
    CONFIG_ATTRS: Incomplete
    def onConnecting(self, transport_details: TransportDetails) -> Optional[ConnectingRequest]: ...
    def onConnect(self, response: ConnectionResponse) -> None: ...
    def startProxyConnect(self) -> None: ...
    data: Incomplete
    state: Incomplete
    def processProxyConnect(self): ...
    def failProxyConnect(self, reason) -> None: ...
    def startHandshake(self): ...
    http_response_data: Incomplete
    websocket_extensions_in_use: Incomplete
    websocket_protocol_in_use: Incomplete
    openHandshakeTimeoutCall: Incomplete
    inside_message: bool
    current_frame: Incomplete
    websocket_version: Incomplete
    autoPingPendingCall: Incomplete
    def processHandshake(self): ...
    wasNotCleanReason: Incomplete
    def failHandshake(self, reason) -> None: ...

class WebSocketClientFactory(WebSocketFactory):
    protocol: Optional[Callable[[], twisted.internet.protocol.Protocol]]
    isServer: bool
    logOctets: bool
    logFrames: bool
    trackTimings: bool
    def __init__(self, url: Incomplete | None = None, origin: Incomplete | None = None, protocols: Incomplete | None = None, useragent=..., headers: Incomplete | None = None, proxy: Incomplete | None = None) -> None: ...
    url: Incomplete
    isSecure: Incomplete
    host: Incomplete
    port: Incomplete
    resource: Incomplete
    path: Incomplete
    params: Incomplete
    origin: Incomplete
    protocols: Incomplete
    useragent: Incomplete
    headers: Incomplete
    proxy: Incomplete
    def setSessionParameters(self, url: Incomplete | None = None, origin: Incomplete | None = None, protocols: Incomplete | None = None, useragent: Incomplete | None = None, headers: Incomplete | None = None, proxy: Incomplete | None = None) -> None: ...
    version: Incomplete
    utf8validateIncoming: bool
    acceptMaskedServerFrames: bool
    maskClientFrames: bool
    applyMask: bool
    maxFramePayloadSize: int
    maxMessagePayloadSize: int
    autoFragmentSize: int
    failByDrop: bool
    echoCloseCodeReason: bool
    serverConnectionDropTimeout: int
    openHandshakeTimeout: int
    closeHandshakeTimeout: int
    tcpNoDelay: bool
    perMessageCompressionOffers: Incomplete
    perMessageCompressionAccept: Incomplete
    autoPingInterval: int
    autoPingTimeout: int
    autoPingSize: int
    autoPingRestartOnAnyTraffic: bool
    def resetProtocolOptions(self) -> None: ...
    def setProtocolOptions(self, version: Incomplete | None = None, utf8validateIncoming: Incomplete | None = None, acceptMaskedServerFrames: Incomplete | None = None, maskClientFrames: Incomplete | None = None, applyMask: Incomplete | None = None, maxFramePayloadSize: Incomplete | None = None, maxMessagePayloadSize: Incomplete | None = None, autoFragmentSize: Incomplete | None = None, failByDrop: Incomplete | None = None, echoCloseCodeReason: Incomplete | None = None, serverConnectionDropTimeout: Incomplete | None = None, openHandshakeTimeout: Incomplete | None = None, closeHandshakeTimeout: Incomplete | None = None, tcpNoDelay: Incomplete | None = None, perMessageCompressionOffers: Incomplete | None = None, perMessageCompressionAccept: Incomplete | None = None, autoPingInterval: Incomplete | None = None, autoPingTimeout: Incomplete | None = None, autoPingSize: Incomplete | None = None, autoPingRestartOnAnyTraffic: Incomplete | None = None) -> None: ...
