from _typeshed import Incomplete
from typing import Any, Dict, Optional

__all__ = ['Message', 'Hello', 'Welcome', 'Abort', 'Challenge', 'Authenticate', 'Goodbye', 'Error', 'Publish', 'Published', 'Subscribe', 'Subscribed', 'Unsubscribe', 'Unsubscribed', 'Event', 'Call', 'Cancel', 'Result', 'Register', 'Registered', 'Unregister', 'Unregistered', 'Invocation', 'Interrupt', 'Yield', 'check_or_raise_uri', 'check_or_raise_realm_name', 'check_or_raise_id', 'check_or_raise_extra', 'is_valid_enc_algo', 'is_valid_enc_serializer', 'identify_realm_name_category', 'PAYLOAD_ENC_CRYPTO_BOX', 'PAYLOAD_ENC_MQTT', 'PAYLOAD_ENC_STANDARD_IDENTIFIERS']

PAYLOAD_ENC_CRYPTO_BOX: str
PAYLOAD_ENC_MQTT: str
PAYLOAD_ENC_STANDARD_IDENTIFIERS: Incomplete

def is_valid_enc_algo(enc_algo): ...
def is_valid_enc_serializer(enc_serializer): ...
def identify_realm_name_category(value: Any) -> Optional[str]: ...
def check_or_raise_uri(value: Any, message: str = 'WAMP message invalid', strict: bool = False, allow_empty_components: bool = False, allow_last_empty: bool = False, allow_none: bool = False) -> str: ...
def check_or_raise_realm_name(value, message: str = 'WAMP message invalid', allow_eth: bool = True): ...
def check_or_raise_id(value: Any, message: str = 'WAMP message invalid') -> int: ...
def check_or_raise_extra(value: Any, message: str = 'WAMP message invalid') -> Dict[str, Any]: ...

class Message:
    MESSAGE_TYPE: Incomplete
    def __init__(self, from_fbs: Incomplete | None = None) -> None: ...
    @property
    def correlation_id(self): ...
    @correlation_id.setter
    def correlation_id(self, value) -> None: ...
    @property
    def correlation_uri(self): ...
    @correlation_uri.setter
    def correlation_uri(self, value) -> None: ...
    @property
    def correlation_is_anchor(self): ...
    @correlation_is_anchor.setter
    def correlation_is_anchor(self, value) -> None: ...
    @property
    def correlation_is_last(self): ...
    @correlation_is_last.setter
    def correlation_is_last(self, value) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    @staticmethod
    def parse(wmsg) -> None: ...
    def marshal(self) -> None: ...
    @staticmethod
    def cast(buf) -> None: ...
    def build(self, builder) -> None: ...
    def uncache(self) -> None: ...
    def serialize(self, serializer): ...

class Hello(Message):
    MESSAGE_TYPE: int
    realm: Incomplete
    roles: Incomplete
    authmethods: Incomplete
    authid: Incomplete
    authrole: Incomplete
    authextra: Incomplete
    resumable: Incomplete
    resume_session: Incomplete
    resume_token: Incomplete
    def __init__(self, realm, roles, authmethods: Incomplete | None = None, authid: Incomplete | None = None, authrole: Incomplete | None = None, authextra: Incomplete | None = None, resumable: Incomplete | None = None, resume_session: Incomplete | None = None, resume_token: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Welcome(Message):
    MESSAGE_TYPE: int
    session: Incomplete
    roles: Incomplete
    realm: Incomplete
    authid: Incomplete
    authrole: Incomplete
    authmethod: Incomplete
    authprovider: Incomplete
    authextra: Incomplete
    resumed: Incomplete
    resumable: Incomplete
    resume_token: Incomplete
    custom: Incomplete
    def __init__(self, session, roles, realm: Incomplete | None = None, authid: Incomplete | None = None, authrole: Incomplete | None = None, authmethod: Incomplete | None = None, authprovider: Incomplete | None = None, authextra: Incomplete | None = None, resumed: Incomplete | None = None, resumable: Incomplete | None = None, resume_token: Incomplete | None = None, custom: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Abort(Message):
    MESSAGE_TYPE: int
    reason: Incomplete
    message: Incomplete
    def __init__(self, reason, message: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Challenge(Message):
    MESSAGE_TYPE: int
    method: Incomplete
    extra: Incomplete
    def __init__(self, method, extra: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Authenticate(Message):
    MESSAGE_TYPE: int
    signature: Incomplete
    extra: Incomplete
    def __init__(self, signature, extra: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Goodbye(Message):
    MESSAGE_TYPE: int
    DEFAULT_REASON: str
    reason: Incomplete
    message: Incomplete
    resumable: Incomplete
    def __init__(self, reason=..., message: Incomplete | None = None, resumable: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Error(Message):
    MESSAGE_TYPE: int
    request_type: Incomplete
    request: Incomplete
    error: Incomplete
    args: Incomplete
    kwargs: Incomplete
    payload: Incomplete
    enc_algo: Incomplete
    enc_key: Incomplete
    enc_serializer: Incomplete
    callee: Incomplete
    callee_authid: Incomplete
    callee_authrole: Incomplete
    forward_for: Incomplete
    def __init__(self, request_type, request, error, args: Incomplete | None = None, kwargs: Incomplete | None = None, payload: Incomplete | None = None, enc_algo: Incomplete | None = None, enc_key: Incomplete | None = None, enc_serializer: Incomplete | None = None, callee: Incomplete | None = None, callee_authid: Incomplete | None = None, callee_authrole: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Publish(Message):
    MESSAGE_TYPE: int
    def __init__(self, request: Incomplete | None = None, topic: Incomplete | None = None, args: Incomplete | None = None, kwargs: Incomplete | None = None, payload: Incomplete | None = None, acknowledge: Incomplete | None = None, exclude_me: Incomplete | None = None, exclude: Incomplete | None = None, exclude_authid: Incomplete | None = None, exclude_authrole: Incomplete | None = None, eligible: Incomplete | None = None, eligible_authid: Incomplete | None = None, eligible_authrole: Incomplete | None = None, retain: Incomplete | None = None, transaction_hash: Incomplete | None = None, enc_algo: Incomplete | None = None, enc_key: Incomplete | None = None, enc_serializer: Incomplete | None = None, forward_for: Incomplete | None = None, from_fbs: Incomplete | None = None) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    @property
    def request(self): ...
    @request.setter
    def request(self, value) -> None: ...
    @property
    def topic(self): ...
    @topic.setter
    def topic(self, value) -> None: ...
    @property
    def args(self): ...
    @args.setter
    def args(self, value) -> None: ...
    @property
    def kwargs(self): ...
    @kwargs.setter
    def kwargs(self, value) -> None: ...
    @property
    def payload(self): ...
    @payload.setter
    def payload(self, value) -> None: ...
    @property
    def acknowledge(self): ...
    @acknowledge.setter
    def acknowledge(self, value) -> None: ...
    @property
    def exclude_me(self): ...
    @exclude_me.setter
    def exclude_me(self, value) -> None: ...
    @property
    def exclude(self): ...
    @exclude.setter
    def exclude(self, value) -> None: ...
    @property
    def exclude_authid(self): ...
    @exclude_authid.setter
    def exclude_authid(self, value) -> None: ...
    @property
    def exclude_authrole(self): ...
    @exclude_authrole.setter
    def exclude_authrole(self, value) -> None: ...
    @property
    def eligible(self): ...
    @eligible.setter
    def eligible(self, value) -> None: ...
    @property
    def eligible_authid(self): ...
    @eligible_authid.setter
    def eligible_authid(self, value) -> None: ...
    @property
    def eligible_authrole(self): ...
    @eligible_authrole.setter
    def eligible_authrole(self, value) -> None: ...
    @property
    def retain(self): ...
    @retain.setter
    def retain(self, value) -> None: ...
    @property
    def transaction_hash(self): ...
    @transaction_hash.setter
    def transaction_hash(self, value) -> None: ...
    @property
    def enc_algo(self): ...
    @enc_algo.setter
    def enc_algo(self, value) -> None: ...
    @property
    def enc_key(self): ...
    @enc_key.setter
    def enc_key(self, value) -> None: ...
    @property
    def enc_serializer(self): ...
    @enc_serializer.setter
    def enc_serializer(self, value) -> None: ...
    @property
    def forward_for(self): ...
    @forward_for.setter
    def forward_for(self, value) -> None: ...
    @staticmethod
    def cast(buf): ...
    def build(self, builder): ...
    @staticmethod
    def parse(wmsg): ...
    def marshal_options(self): ...
    def marshal(self): ...

class Published(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    publication: Incomplete
    def __init__(self, request, publication) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Subscribe(Message):
    MESSAGE_TYPE: int
    MATCH_EXACT: str
    MATCH_PREFIX: str
    MATCH_WILDCARD: str
    request: Incomplete
    topic: Incomplete
    match: Incomplete
    get_retained: Incomplete
    forward_for: Incomplete
    def __init__(self, request, topic, match: Incomplete | None = None, get_retained: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal_options(self): ...
    def marshal(self): ...

class Subscribed(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    subscription: Incomplete
    def __init__(self, request, subscription) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Unsubscribe(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    subscription: Incomplete
    forward_for: Incomplete
    def __init__(self, request, subscription, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Unsubscribed(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    subscription: Incomplete
    reason: Incomplete
    def __init__(self, request, subscription: Incomplete | None = None, reason: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Event(Message):
    MESSAGE_TYPE: int
    def __init__(self, subscription: Incomplete | None = None, publication: Incomplete | None = None, args: Incomplete | None = None, kwargs: Incomplete | None = None, payload: Incomplete | None = None, publisher: Incomplete | None = None, publisher_authid: Incomplete | None = None, publisher_authrole: Incomplete | None = None, topic: Incomplete | None = None, retained: Incomplete | None = None, transaction_hash: Incomplete | None = None, x_acknowledged_delivery: Incomplete | None = None, enc_algo: Incomplete | None = None, enc_key: Incomplete | None = None, enc_serializer: Incomplete | None = None, forward_for: Incomplete | None = None, from_fbs: Incomplete | None = None) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    @property
    def subscription(self): ...
    @subscription.setter
    def subscription(self, value) -> None: ...
    @property
    def publication(self): ...
    @publication.setter
    def publication(self, value) -> None: ...
    @property
    def args(self): ...
    @args.setter
    def args(self, value) -> None: ...
    @property
    def kwargs(self): ...
    @kwargs.setter
    def kwargs(self, value) -> None: ...
    @property
    def payload(self): ...
    @payload.setter
    def payload(self, value) -> None: ...
    @property
    def publisher(self): ...
    @publisher.setter
    def publisher(self, value) -> None: ...
    @property
    def publisher_authid(self): ...
    @publisher_authid.setter
    def publisher_authid(self, value) -> None: ...
    @property
    def publisher_authrole(self): ...
    @publisher_authrole.setter
    def publisher_authrole(self, value) -> None: ...
    @property
    def topic(self): ...
    @topic.setter
    def topic(self, value) -> None: ...
    @property
    def retained(self): ...
    @retained.setter
    def retained(self, value) -> None: ...
    @property
    def transaction_hash(self): ...
    @transaction_hash.setter
    def transaction_hash(self, value) -> None: ...
    @property
    def x_acknowledged_delivery(self): ...
    @x_acknowledged_delivery.setter
    def x_acknowledged_delivery(self, value) -> None: ...
    @property
    def enc_algo(self): ...
    @enc_algo.setter
    def enc_algo(self, value) -> None: ...
    @property
    def enc_key(self): ...
    @enc_key.setter
    def enc_key(self, value) -> None: ...
    @property
    def enc_serializer(self): ...
    @enc_serializer.setter
    def enc_serializer(self, value) -> None: ...
    @property
    def forward_for(self): ...
    @forward_for.setter
    def forward_for(self, value) -> None: ...
    @staticmethod
    def cast(buf): ...
    def build(self, builder): ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class EventReceived(Message):
    MESSAGE_TYPE: int
    publication: Incomplete
    def __init__(self, publication) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Call(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    procedure: Incomplete
    args: Incomplete
    kwargs: Incomplete
    payload: Incomplete
    timeout: Incomplete
    receive_progress: Incomplete
    transaction_hash: Incomplete
    enc_algo: Incomplete
    enc_key: Incomplete
    enc_serializer: Incomplete
    caller: Incomplete
    caller_authid: Incomplete
    caller_authrole: Incomplete
    forward_for: Incomplete
    def __init__(self, request, procedure, args: Incomplete | None = None, kwargs: Incomplete | None = None, payload: Incomplete | None = None, timeout: Incomplete | None = None, receive_progress: Incomplete | None = None, transaction_hash: Incomplete | None = None, enc_algo: Incomplete | None = None, enc_key: Incomplete | None = None, enc_serializer: Incomplete | None = None, caller: Incomplete | None = None, caller_authid: Incomplete | None = None, caller_authrole: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal_options(self): ...
    def marshal(self): ...

class Cancel(Message):
    MESSAGE_TYPE: int
    SKIP: str
    KILL: str
    KILLNOWAIT: str
    request: Incomplete
    mode: Incomplete
    forward_for: Incomplete
    def __init__(self, request, mode: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Result(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    args: Incomplete
    kwargs: Incomplete
    payload: Incomplete
    progress: Incomplete
    enc_algo: Incomplete
    enc_key: Incomplete
    enc_serializer: Incomplete
    callee: Incomplete
    callee_authid: Incomplete
    callee_authrole: Incomplete
    forward_for: Incomplete
    def __init__(self, request, args: Incomplete | None = None, kwargs: Incomplete | None = None, payload: Incomplete | None = None, progress: Incomplete | None = None, enc_algo: Incomplete | None = None, enc_key: Incomplete | None = None, enc_serializer: Incomplete | None = None, callee: Incomplete | None = None, callee_authid: Incomplete | None = None, callee_authrole: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Register(Message):
    MESSAGE_TYPE: int
    MATCH_EXACT: str
    MATCH_PREFIX: str
    MATCH_WILDCARD: str
    INVOKE_SINGLE: str
    INVOKE_FIRST: str
    INVOKE_LAST: str
    INVOKE_ROUNDROBIN: str
    INVOKE_RANDOM: str
    INVOKE_ALL: str
    request: Incomplete
    procedure: Incomplete
    match: Incomplete
    invoke: Incomplete
    concurrency: Incomplete
    force_reregister: Incomplete
    forward_for: Incomplete
    def __init__(self, request, procedure, match: Incomplete | None = None, invoke: Incomplete | None = None, concurrency: Incomplete | None = None, force_reregister: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal_options(self): ...
    def marshal(self): ...

class Registered(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    registration: Incomplete
    def __init__(self, request, registration) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Unregister(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    registration: Incomplete
    forward_for: Incomplete
    def __init__(self, request, registration, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Unregistered(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    registration: Incomplete
    reason: Incomplete
    def __init__(self, request, registration: Incomplete | None = None, reason: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Invocation(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    registration: Incomplete
    args: Incomplete
    kwargs: Incomplete
    payload: Incomplete
    timeout: Incomplete
    receive_progress: Incomplete
    caller: Incomplete
    caller_authid: Incomplete
    caller_authrole: Incomplete
    procedure: Incomplete
    transaction_hash: Incomplete
    enc_algo: Incomplete
    enc_key: Incomplete
    enc_serializer: Incomplete
    forward_for: Incomplete
    def __init__(self, request, registration, args: Incomplete | None = None, kwargs: Incomplete | None = None, payload: Incomplete | None = None, timeout: Incomplete | None = None, receive_progress: Incomplete | None = None, caller: Incomplete | None = None, caller_authid: Incomplete | None = None, caller_authrole: Incomplete | None = None, procedure: Incomplete | None = None, transaction_hash: Incomplete | None = None, enc_algo: Incomplete | None = None, enc_key: Incomplete | None = None, enc_serializer: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Interrupt(Message):
    MESSAGE_TYPE: int
    KILL: str
    KILLNOWAIT: str
    request: Incomplete
    mode: Incomplete
    reason: Incomplete
    forward_for: Incomplete
    def __init__(self, request, mode: Incomplete | None = None, reason: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...

class Yield(Message):
    MESSAGE_TYPE: int
    request: Incomplete
    args: Incomplete
    kwargs: Incomplete
    payload: Incomplete
    progress: Incomplete
    enc_algo: Incomplete
    enc_key: Incomplete
    enc_serializer: Incomplete
    callee: Incomplete
    callee_authid: Incomplete
    callee_authrole: Incomplete
    forward_for: Incomplete
    def __init__(self, request, args: Incomplete | None = None, kwargs: Incomplete | None = None, payload: Incomplete | None = None, progress: Incomplete | None = None, enc_algo: Incomplete | None = None, enc_key: Incomplete | None = None, enc_serializer: Incomplete | None = None, callee: Incomplete | None = None, callee_authid: Incomplete | None = None, callee_authrole: Incomplete | None = None, forward_for: Incomplete | None = None) -> None: ...
    @staticmethod
    def parse(wmsg): ...
    def marshal(self): ...
