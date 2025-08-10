import enum
import typing
from . import network as network
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class CertificateId(int):
    def to_json(self) -> int: ...
    @classmethod
    def from_json(cls, json: int) -> CertificateId: ...

class MixedContentType(enum.Enum):
    BLOCKABLE = 'blockable'
    OPTIONALLY_BLOCKABLE = 'optionally-blockable'
    NONE = 'none'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> MixedContentType: ...

class SecurityState(enum.Enum):
    UNKNOWN = 'unknown'
    NEUTRAL = 'neutral'
    INSECURE = 'insecure'
    SECURE = 'secure'
    INFO = 'info'
    INSECURE_BROKEN = 'insecure-broken'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SecurityState: ...

@dataclass
class CertificateSecurityState:
    protocol: str
    key_exchange: str
    cipher: str
    certificate: list[str]
    subject_name: str
    issuer: str
    valid_from: network.TimeSinceEpoch
    valid_to: network.TimeSinceEpoch
    certificate_has_weak_signature: bool
    certificate_has_sha1_signature: bool
    modern_ssl: bool
    obsolete_ssl_protocol: bool
    obsolete_ssl_key_exchange: bool
    obsolete_ssl_cipher: bool
    obsolete_ssl_signature: bool
    key_exchange_group: str | None = ...
    mac: str | None = ...
    certificate_network_error: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CertificateSecurityState: ...

class SafetyTipStatus(enum.Enum):
    BAD_REPUTATION = 'badReputation'
    LOOKALIKE = 'lookalike'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SafetyTipStatus: ...

@dataclass
class SafetyTipInfo:
    safety_tip_status: SafetyTipStatus
    safe_url: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SafetyTipInfo: ...

@dataclass
class VisibleSecurityState:
    security_state: SecurityState
    security_state_issue_ids: list[str]
    certificate_security_state: CertificateSecurityState | None = ...
    safety_tip_info: SafetyTipInfo | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> VisibleSecurityState: ...

@dataclass
class SecurityStateExplanation:
    security_state: SecurityState
    title: str
    summary: str
    description: str
    mixed_content_type: MixedContentType
    certificate: list[str]
    recommendations: list[str] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SecurityStateExplanation: ...

@dataclass
class InsecureContentStatus:
    ran_mixed_content: bool
    displayed_mixed_content: bool
    contained_mixed_form: bool
    ran_content_with_cert_errors: bool
    displayed_content_with_cert_errors: bool
    ran_insecure_content_style: SecurityState
    displayed_insecure_content_style: SecurityState
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InsecureContentStatus: ...

class CertificateErrorAction(enum.Enum):
    CONTINUE = 'continue'
    CANCEL = 'cancel'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CertificateErrorAction: ...

def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_ignore_certificate_errors(ignore: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def handle_certificate_error(event_id: int, action: CertificateErrorAction) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_override_certificate_errors(override: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class CertificateError:
    event_id: int
    error_type: str
    request_url: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CertificateError: ...

@dataclass
class VisibleSecurityStateChanged:
    visible_security_state: VisibleSecurityState
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> VisibleSecurityStateChanged: ...

@dataclass
class SecurityStateChanged:
    security_state: SecurityState
    scheme_is_cryptographic: bool
    explanations: list[SecurityStateExplanation]
    insecure_content_status: InsecureContentStatus
    summary: str | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SecurityStateChanged: ...
