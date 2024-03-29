import abc
from _typeshed import Incomplete
from autobahn.wamp.message import Welcome
from autobahn.wamp.types import CallResult, Challenge, CloseDetails, ComponentConfig, Publication, RegisterOptions, Registration, SessionDetails, SubscribeOptions, Subscription, TransportDetails
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

__all__ = ['IObjectSerializer', 'ISerializer', 'IMessage', 'ITransport', 'ITransportHandler', 'ISession', 'IAuthenticator', 'IKey', 'ICryptosignKey', 'IEthereumKey', 'ISecurityModule', 'IPayloadCodec']

class IObjectSerializer(abc.ABC, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def NAME(self) -> str: ...
    @property
    @abc.abstractmethod
    def BINARY(self) -> bool: ...
    @abc.abstractmethod
    def serialize(self, obj: Any) -> bytes: ...
    @abc.abstractmethod
    def unserialize(self, payload: bytes) -> List[Any]: ...

class ISerializer(abc.ABC, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def MESSAGE_TYPE_MAP(self) -> Dict[int, 'IMessage']: ...
    @property
    @abc.abstractmethod
    def SERIALIZER_ID(self) -> str: ...
    @property
    @abc.abstractmethod
    def RAWSOCKET_SERIALIZER_ID(self) -> int: ...
    @property
    @abc.abstractmethod
    def MIME_TYPE(self) -> str: ...
    @abc.abstractmethod
    def serialize(self, message: IMessage) -> Tuple[bytes, bool]: ...
    @abc.abstractmethod
    def unserialize(self, payload: bytes, is_binary: Optional[bool] = None) -> List['IMessage']: ...

class IMessage(abc.ABC, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def MESSAGE_TYPE(self) -> int: ...
    @staticmethod
    @abc.abstractmethod
    def parse(wmsg) -> IMessage: ...
    @abc.abstractmethod
    def serialize(self, serializer: ISerializer) -> bytes: ...
    @abc.abstractmethod
    def uncache(self): ...

class ITransport(abc.ABC, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send(self, message: IMessage): ...
    @abc.abstractmethod
    def isOpen(self) -> bool: ...
    @property
    @abc.abstractmethod
    def transport_details(self) -> Optional[TransportDetails]: ...
    @abc.abstractmethod
    def close(self): ...
    @abc.abstractmethod
    def abort(self): ...

class ITransportHandler(abc.ABC, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def onOpen(self, transport: ITransport): ...
    @abc.abstractmethod
    def onMessage(self, message: IMessage): ...
    @abc.abstractmethod
    def onClose(self, wasClean: bool): ...

class _ABC(abc.ABC):
    abc_register: Incomplete

class ISession(_ABC, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def config(self) -> ComponentConfig: ...
    @property
    @abc.abstractmethod
    def transport(self) -> Optional[ITransport]: ...
    @property
    @abc.abstractmethod
    def session_details(self) -> Optional[SessionDetails]: ...
    @abc.abstractmethod
    def onUserError(self, fail, msg): ...
    @abc.abstractmethod
    def onConnect(self): ...
    @abc.abstractmethod
    def join(self, realm: str, authmethods: Optional[List[str]] = None, authid: Optional[str] = None, authrole: Optional[str] = None, authextra: Optional[Dict[str, Any]] = None, resumable: Optional[bool] = None, resume_session: Optional[int] = None, resume_token: Optional[str] = None): ...
    @abc.abstractmethod
    def onChallenge(self, challenge: Challenge) -> str: ...
    @abc.abstractmethod
    def onWelcome(self, welcome: Welcome) -> Optional[str]: ...
    @abc.abstractmethod
    def onJoin(self, details: SessionDetails): ...
    @abc.abstractmethod
    def leave(self, reason: Optional[str] = None, message: Optional[str] = None): ...
    @abc.abstractmethod
    def onLeave(self, details: CloseDetails): ...
    @abc.abstractmethod
    def disconnect(self): ...
    @abc.abstractmethod
    def onDisconnect(self): ...
    @abc.abstractmethod
    def is_connected(self) -> bool: ...
    @abc.abstractmethod
    def is_attached(self) -> bool: ...
    @abc.abstractmethod
    def set_payload_codec(self, payload_codec: Optional['IPayloadCodec']): ...
    @abc.abstractmethod
    def get_payload_codec(self) -> Optional['IPayloadCodec']: ...
    @abc.abstractmethod
    def define(self, exception: Exception, error: Optional[str] = None): ...
    @abc.abstractmethod
    def call(self, procedure: str, *args, **kwargs) -> Union[Any, CallResult]: ...
    @abc.abstractmethod
    def register(self, endpoint: Union[Callable, Any], procedure: Optional[str] = None, options: Optional[RegisterOptions] = None, prefix: Optional[str] = None, check_types: Optional[bool] = None) -> Union[Registration, List[Registration]]: ...
    @abc.abstractmethod
    def publish(self, topic: str, *args, **kwargs) -> Optional[Publication]: ...
    @abc.abstractmethod
    def subscribe(self, handler: Union[Callable, Any], topic: Optional[str] = None, options: Optional[SubscribeOptions] = None, check_types: Optional[bool] = None) -> Union[Subscription, List[Subscription]]: ...

class IAuthenticator(abc.ABC, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def on_challenge(self, session: ISession, challenge: Challenge): ...
    @abc.abstractmethod
    def on_welcome(self, authextra: Optional[Dict[str, Any]]) -> Optional[str]: ...

class IKey(abc.ABC, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def security_module(self) -> Optional['ISecurityModule']: ...
    @property
    @abc.abstractmethod
    def key_no(self) -> Optional[int]: ...
    @property
    @abc.abstractmethod
    def key_type(self) -> str: ...
    @abc.abstractmethod
    def public_key(self, binary: bool = False) -> Union[str, bytes]: ...
    @abc.abstractmethod
    def can_sign(self) -> bool: ...
    @abc.abstractmethod
    def sign(self, data: bytes) -> bytes: ...
    @abc.abstractmethod
    def recover(self, data: bytes, signature: bytes) -> bytes: ...

class ICryptosignKey(IKey, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def sign_challenge(self, challenge: Challenge, channel_id: Optional[bytes] = None, channel_id_type: Optional[str] = None) -> bytes: ...
    @abc.abstractmethod
    def verify_challenge(self, challenge: Challenge, signature: bytes, channel_id: Optional[bytes] = None, channel_id_type: Optional[str] = None) -> bool: ...

class IEthereumKey(IKey, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def address(self, binary: bool = False) -> Union[str, bytes]: ...
    @abc.abstractmethod
    def sign_typed_data(self, data: Dict[str, Any]) -> bytes: ...
    @abc.abstractmethod
    def verify_typed_data(self, data: Dict[str, Any], signature: bytes, signer_address: Union[str, bytes]) -> bool: ...

class ISecurityModule(abc.ABC, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __len__(self) -> int: ...
    @abc.abstractmethod
    def __contains__(self, key_no: int) -> bool: ...
    @abc.abstractmethod
    def __getitem__(self, key_no: int) -> Union[ICryptosignKey, IEthereumKey]: ...
    @abc.abstractmethod
    def __setitem__(self, key_no: int, key: Union[ICryptosignKey, IEthereumKey]) -> None: ...
    @abc.abstractmethod
    def __delitem__(self, key_no: int) -> None: ...
    @abc.abstractmethod
    def open(self): ...
    @abc.abstractmethod
    def close(self): ...
    @property
    @abc.abstractmethod
    def is_open(self) -> bool: ...
    @property
    @abc.abstractmethod
    def can_lock(self) -> bool: ...
    @property
    @abc.abstractmethod
    def is_locked(self) -> bool: ...
    @abc.abstractmethod
    def lock(self): ...
    @abc.abstractmethod
    def unlock(self): ...
    @abc.abstractmethod
    def create_key(self, key_type: str) -> int: ...
    @abc.abstractmethod
    def delete_key(self, key_no: int): ...
    @abc.abstractmethod
    def get_random(self, octets: int) -> bytes: ...
    @abc.abstractmethod
    def get_counter(self, counter_no: int) -> int: ...
    @abc.abstractmethod
    def increment_counter(self, counter_no: int) -> int: ...

class IPayloadCodec(abc.ABC, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encode(self, is_originating, uri, args: Incomplete | None = None, kwargs: Incomplete | None = None): ...
    @abc.abstractmethod
    def decode(self, is_originating, uri, encoded_payload): ...
