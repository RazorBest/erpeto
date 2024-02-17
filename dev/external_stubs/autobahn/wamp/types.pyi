from _typeshed import Incomplete
from autobahn.wamp.request import Publication as Publication, Registration as Registration, Subscription as Subscription
from typing import Any, Dict, List, Optional

__all__ = ['ComponentConfig', 'HelloReturn', 'Accept', 'Deny', 'Challenge', 'HelloDetails', 'SessionIdent', 'CloseDetails', 'SubscribeOptions', 'EventDetails', 'PublishOptions', 'RegisterOptions', 'CallDetails', 'CallOptions', 'CallResult', 'EncodedPayload', 'Subscription', 'Registration', 'Publication', 'TransportDetails', 'SessionDetails']

class ComponentConfig:
    realm: Incomplete
    extra: Incomplete
    keyring: Incomplete
    controller: Incomplete
    shared: Incomplete
    runner: Incomplete
    def __init__(self, realm: Incomplete | None = None, extra: Incomplete | None = None, keyring: Incomplete | None = None, controller: Incomplete | None = None, shared: Incomplete | None = None, runner: Incomplete | None = None) -> None: ...

class HelloReturn: ...

class Accept(HelloReturn):
    realm: Incomplete
    authid: Incomplete
    authrole: Incomplete
    authmethod: Incomplete
    authprovider: Incomplete
    authextra: Incomplete
    def __init__(self, realm: Optional[str] = None, authid: Optional[str] = None, authrole: Optional[str] = None, authmethod: Optional[str] = None, authprovider: Optional[str] = None, authextra: Optional[Dict[str, Any]] = None) -> None: ...

class Deny(HelloReturn):
    reason: Incomplete
    message: Incomplete
    def __init__(self, reason: str = 'wamp.error.not_authorized', message: Incomplete | None = None) -> None: ...

class Challenge(HelloReturn):
    method: Incomplete
    extra: Incomplete
    def __init__(self, method, extra: Incomplete | None = None) -> None: ...

class HelloDetails:
    realm: Incomplete
    authmethods: Incomplete
    authid: Incomplete
    authrole: Incomplete
    authextra: Incomplete
    session_roles: Incomplete
    pending_session: Incomplete
    resumable: Incomplete
    resume_session: Incomplete
    resume_token: Incomplete
    def __init__(self, realm: Incomplete | None = None, authmethods: Incomplete | None = None, authid: Incomplete | None = None, authrole: Incomplete | None = None, authextra: Incomplete | None = None, session_roles: Incomplete | None = None, pending_session: Incomplete | None = None, resumable: Incomplete | None = None, resume_session: Incomplete | None = None, resume_token: Incomplete | None = None) -> None: ...

class SessionIdent:
    session: Incomplete
    authid: Incomplete
    authrole: Incomplete
    def __init__(self, session: Incomplete | None = None, authid: Incomplete | None = None, authrole: Incomplete | None = None) -> None: ...
    def marshal(self): ...
    @staticmethod
    def from_calldetails(call_details): ...
    @staticmethod
    def from_eventdetails(event_details): ...

class CloseDetails:
    REASON_DEFAULT: str
    REASON_TRANSPORT_LOST: str
    reason: Incomplete
    message: Incomplete
    def __init__(self, reason: Incomplete | None = None, message: Incomplete | None = None) -> None: ...
    def marshal(self): ...

class SubscribeOptions:
    match: Incomplete
    details: Incomplete
    details_arg: str
    get_retained: Incomplete
    forward_for: Incomplete
    correlation_id: Incomplete
    correlation_uri: Incomplete
    correlation_is_anchor: Incomplete
    correlation_is_last: Incomplete
    def __init__(self, match: Incomplete | None = None, details: Incomplete | None = None, details_arg: Incomplete | None = None, forward_for: Incomplete | None = None, get_retained: Incomplete | None = None, correlation_id: Incomplete | None = None, correlation_uri: Incomplete | None = None, correlation_is_anchor: Incomplete | None = None, correlation_is_last: Incomplete | None = None) -> None: ...
    def message_attr(self): ...

class EventDetails:
    subscription: Incomplete
    publication: Incomplete
    publisher: Incomplete
    publisher_authid: Incomplete
    publisher_authrole: Incomplete
    topic: Incomplete
    retained: Incomplete
    transaction_hash: Incomplete
    enc_algo: Incomplete
    forward_for: Incomplete
    def __init__(self, subscription, publication, publisher: Incomplete | None = None, publisher_authid: Incomplete | None = None, publisher_authrole: Incomplete | None = None, topic: Incomplete | None = None, retained: Incomplete | None = None, transaction_hash: Incomplete | None = None, enc_algo: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...

class PublishOptions:
    acknowledge: Incomplete
    exclude_me: Incomplete
    exclude: Incomplete
    exclude_authid: Incomplete
    exclude_authrole: Incomplete
    eligible: Incomplete
    eligible_authid: Incomplete
    eligible_authrole: Incomplete
    retain: Incomplete
    transaction_hash: Incomplete
    forward_for: Incomplete
    correlation_id: Incomplete
    correlation_uri: Incomplete
    correlation_is_anchor: Incomplete
    correlation_is_last: Incomplete
    def __init__(self, acknowledge: Incomplete | None = None, exclude_me: Incomplete | None = None, exclude: Incomplete | None = None, exclude_authid: Incomplete | None = None, exclude_authrole: Incomplete | None = None, eligible: Incomplete | None = None, eligible_authid: Incomplete | None = None, eligible_authrole: Incomplete | None = None, retain: Incomplete | None = None, forward_for: Incomplete | None = None, transaction_hash: Incomplete | None = None, correlation_id: Incomplete | None = None, correlation_uri: Incomplete | None = None, correlation_is_anchor: Incomplete | None = None, correlation_is_last: Incomplete | None = None) -> None: ...
    def message_attr(self): ...

class RegisterOptions:
    match: Incomplete
    invoke: Incomplete
    concurrency: Incomplete
    force_reregister: Incomplete
    forward_for: Incomplete
    details: Incomplete
    details_arg: str
    correlation_id: Incomplete
    correlation_uri: Incomplete
    correlation_is_anchor: Incomplete
    correlation_is_last: Incomplete
    def __init__(self, match: Incomplete | None = None, invoke: Incomplete | None = None, concurrency: Incomplete | None = None, force_reregister: Incomplete | None = None, forward_for: Incomplete | None = None, details: Incomplete | None = None, details_arg: Incomplete | None = None, correlation_id: Incomplete | None = None, correlation_uri: Incomplete | None = None, correlation_is_anchor: Incomplete | None = None, correlation_is_last: Incomplete | None = None) -> None: ...
    def message_attr(self): ...

class CallDetails:
    registration: Incomplete
    progress: Incomplete
    caller: Incomplete
    caller_authid: Incomplete
    caller_authrole: Incomplete
    procedure: Incomplete
    transaction_hash: Incomplete
    enc_algo: Incomplete
    forward_for: Incomplete
    def __init__(self, registration, progress: Incomplete | None = None, caller: Incomplete | None = None, caller_authid: Incomplete | None = None, caller_authrole: Incomplete | None = None, procedure: Incomplete | None = None, transaction_hash: Incomplete | None = None, enc_algo: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...

class CallOptions:
    on_progress: Incomplete
    timeout: Incomplete
    transaction_hash: Incomplete
    caller: Incomplete
    caller_authid: Incomplete
    caller_authrole: Incomplete
    forward_for: Incomplete
    details: Incomplete
    correlation_id: Incomplete
    correlation_uri: Incomplete
    correlation_is_anchor: Incomplete
    correlation_is_last: Incomplete
    def __init__(self, on_progress: Incomplete | None = None, timeout: Incomplete | None = None, transaction_hash: Incomplete | None = None, caller: Incomplete | None = None, caller_authid: Incomplete | None = None, caller_authrole: Incomplete | None = None, forward_for: Incomplete | None = None, correlation_id: Incomplete | None = None, correlation_uri: Incomplete | None = None, correlation_is_anchor: Incomplete | None = None, correlation_is_last: Incomplete | None = None, details: Incomplete | None = None) -> None: ...
    def message_attr(self): ...

class CallResult:
    enc_algo: Incomplete
    callee: Incomplete
    callee_authid: Incomplete
    callee_authrole: Incomplete
    forward_for: Incomplete
    results: Incomplete
    kwresults: Incomplete
    def __init__(self, *results, **kwresults) -> None: ...

class EncodedPayload:
    payload: Incomplete
    enc_algo: Incomplete
    enc_serializer: Incomplete
    enc_key: Incomplete
    def __init__(self, payload, enc_algo, enc_serializer: Incomplete | None = None, enc_key: Incomplete | None = None) -> None: ...

class IPublication:
    def id(self) -> None: ...

class ISubscription:
    def id(self) -> None: ...
    def active(self) -> None: ...
    def unsubscribe(self) -> None: ...

class IRegistration:
    def id(self) -> None: ...
    def active(self) -> None: ...
    def unregister(self) -> None: ...

class TransportDetails:
    CHANNEL_TYPE_NONE: int
    CHANNEL_TYPE_FUNCTION: int
    CHANNEL_TYPE_MEMORY: int
    CHANNEL_TYPE_SERIAL: int
    CHANNEL_TYPE_TCP: int
    CHANNEL_TYPE_TLS: int
    CHANNEL_TYPE_UDP: int
    CHANNEL_TYPE_DTLS: int
    CHANNEL_TYPE_TO_STR: Incomplete
    CHANNEL_TYPE_FROM_STR: Incomplete
    CHANNEL_FRAMING_NONE: int
    CHANNEL_FRAMING_NATIVE: int
    CHANNEL_FRAMING_WEBSOCKET: int
    CHANNEL_FRAMING_RAWSOCKET: int
    CHANNEL_FRAMING_TO_STR: Incomplete
    CHANNEL_FRAMING_FROM_STR: Incomplete
    CHANNEL_SERIALIZER_NONE: int
    CHANNEL_SERIALIZER_JSON: int
    CHANNEL_SERIALIZER_MSGPACK: int
    CHANNEL_SERIALIZER_CBOR: int
    CHANNEL_SERIALIZER_UBJSON: int
    CHANNEL_SERIALIZER_FLATBUFFERS: int
    CHANNEL_SERIALIZER_TO_STR: Incomplete
    CHANNEL_SERIALIZER_FROM_STR: Incomplete
    def __init__(self, channel_type: Optional[int] = None, channel_framing: Optional[int] = None, channel_serializer: Optional[int] = None, own: Optional[str] = None, peer: Optional[str] = None, is_server: Optional[bool] = None, own_pid: Optional[int] = None, own_tid: Optional[int] = None, own_fd: Optional[int] = None, is_secure: Optional[bool] = None, channel_id: Optional[Dict[str, bytes]] = None, peer_cert: Optional[Dict[str, Any]] = None, websocket_protocol: Optional[str] = None, websocket_extensions_in_use: Optional[List[str]] = None, http_headers_received: Optional[Dict[str, Any]] = None, http_headers_sent: Optional[Dict[str, Any]] = None, http_cbtid: Optional[str] = None) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    @staticmethod
    def parse(data: Dict[str, Any]) -> TransportDetails: ...
    def marshal(self) -> Dict[str, Any]: ...
    @property
    def channel_typeid(self): ...
    @property
    def channel_type(self) -> Optional[int]: ...
    @channel_type.setter
    def channel_type(self, value: Optional[int]): ...
    @property
    def channel_framing(self) -> Optional[int]: ...
    @channel_framing.setter
    def channel_framing(self, value: Optional[int]): ...
    @property
    def channel_serializer(self) -> Optional[int]: ...
    @channel_serializer.setter
    def channel_serializer(self, value: Optional[int]): ...
    @property
    def own(self) -> Optional[str]: ...
    @own.setter
    def own(self, value: Optional[str]): ...
    @property
    def peer(self) -> Optional[str]: ...
    @peer.setter
    def peer(self, value: Optional[str]): ...
    @property
    def is_server(self) -> Optional[bool]: ...
    @is_server.setter
    def is_server(self, value: Optional[bool]): ...
    @property
    def own_pid(self) -> Optional[int]: ...
    @own_pid.setter
    def own_pid(self, value: Optional[int]): ...
    @property
    def own_tid(self) -> Optional[int]: ...
    @own_tid.setter
    def own_tid(self, value: Optional[int]): ...
    @property
    def own_fd(self) -> Optional[int]: ...
    @own_fd.setter
    def own_fd(self, value: Optional[int]): ...
    @property
    def is_secure(self) -> Optional[bool]: ...
    @is_secure.setter
    def is_secure(self, value: Optional[bool]): ...
    @property
    def channel_id(self) -> Dict[str, bytes]: ...
    @channel_id.setter
    def channel_id(self, value: Dict[str, bytes]): ...
    @property
    def peer_cert(self) -> Dict[str, Any]: ...
    @peer_cert.setter
    def peer_cert(self, value: Dict[str, Any]): ...
    @property
    def websocket_protocol(self) -> Optional[str]: ...
    @websocket_protocol.setter
    def websocket_protocol(self, value: Optional[str]): ...
    @property
    def websocket_extensions_in_use(self) -> Optional[List[str]]: ...
    @websocket_extensions_in_use.setter
    def websocket_extensions_in_use(self, value: Optional[List[str]]): ...
    @property
    def http_headers_received(self) -> Dict[str, Any]: ...
    @http_headers_received.setter
    def http_headers_received(self, value: Dict[str, Any]): ...
    @property
    def http_headers_sent(self) -> Dict[str, Any]: ...
    @http_headers_sent.setter
    def http_headers_sent(self, value: Dict[str, Any]): ...
    @property
    def http_cbtid(self) -> Optional[str]: ...
    @http_cbtid.setter
    def http_cbtid(self, value: Optional[str]): ...

class SessionDetails:
    def __init__(self, realm: Optional[str] = None, session: Optional[int] = None, authid: Optional[str] = None, authrole: Optional[str] = None, authmethod: Optional[str] = None, authprovider: Optional[str] = None, authextra: Optional[Dict[str, Any]] = None, serializer: Optional[str] = None, transport: Optional[TransportDetails] = None, resumed: Optional[bool] = None, resumable: Optional[bool] = None, resume_token: Optional[str] = None) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    @staticmethod
    def parse(data: Dict[str, Any]) -> SessionDetails: ...
    def marshal(self) -> Dict[str, Any]: ...
    @property
    def realm(self) -> Optional[str]: ...
    @realm.setter
    def realm(self, value: Optional[str]): ...
    @property
    def session(self) -> Optional[int]: ...
    @session.setter
    def session(self, value: Optional[int]): ...
    @property
    def authid(self) -> Optional[str]: ...
    @authid.setter
    def authid(self, value: Optional[str]): ...
    @property
    def authrole(self) -> Optional[str]: ...
    @authrole.setter
    def authrole(self, value: Optional[str]): ...
    @property
    def authmethod(self) -> Optional[str]: ...
    @authmethod.setter
    def authmethod(self, value: Optional[str]): ...
    @property
    def authprovider(self) -> Optional[str]: ...
    @authprovider.setter
    def authprovider(self, value: Optional[str]): ...
    @property
    def authextra(self) -> Optional[Dict[str, Any]]: ...
    @authextra.setter
    def authextra(self, value: Optional[Dict[str, Any]]): ...
    @property
    def serializer(self) -> Optional[str]: ...
    @serializer.setter
    def serializer(self, value: Optional[str]): ...
    @property
    def transport(self) -> Optional[TransportDetails]: ...
    @transport.setter
    def transport(self, value: Optional[TransportDetails]): ...
    @property
    def resumed(self) -> Optional[bool]: ...
    @resumed.setter
    def resumed(self, value: Optional[bool]): ...
    @property
    def resumable(self) -> Optional[bool]: ...
    @resumable.setter
    def resumable(self, value: Optional[bool]): ...
    @property
    def resume_token(self) -> Optional[str]: ...
    @resume_token.setter
    def resume_token(self, value: Optional[str]): ...
