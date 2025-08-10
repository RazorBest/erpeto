import enum
import typing
from . import debugger as debugger, emulation as emulation, io as io, page as page, runtime as runtime, security as security
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class ResourceType(enum.Enum):
    DOCUMENT = 'Document'
    STYLESHEET = 'Stylesheet'
    IMAGE = 'Image'
    MEDIA = 'Media'
    FONT = 'Font'
    SCRIPT = 'Script'
    TEXT_TRACK = 'TextTrack'
    XHR = 'XHR'
    FETCH = 'Fetch'
    PREFETCH = 'Prefetch'
    EVENT_SOURCE = 'EventSource'
    WEB_SOCKET = 'WebSocket'
    MANIFEST = 'Manifest'
    SIGNED_EXCHANGE = 'SignedExchange'
    PING = 'Ping'
    CSP_VIOLATION_REPORT = 'CSPViolationReport'
    PREFLIGHT = 'Preflight'
    FED_CM = 'FedCM'
    OTHER = 'Other'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ResourceType: ...

class LoaderId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> LoaderId: ...

class RequestId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> RequestId: ...

class InterceptionId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> InterceptionId: ...

class ErrorReason(enum.Enum):
    FAILED = 'Failed'
    ABORTED = 'Aborted'
    TIMED_OUT = 'TimedOut'
    ACCESS_DENIED = 'AccessDenied'
    CONNECTION_CLOSED = 'ConnectionClosed'
    CONNECTION_RESET = 'ConnectionReset'
    CONNECTION_REFUSED = 'ConnectionRefused'
    CONNECTION_ABORTED = 'ConnectionAborted'
    CONNECTION_FAILED = 'ConnectionFailed'
    NAME_NOT_RESOLVED = 'NameNotResolved'
    INTERNET_DISCONNECTED = 'InternetDisconnected'
    ADDRESS_UNREACHABLE = 'AddressUnreachable'
    BLOCKED_BY_CLIENT = 'BlockedByClient'
    BLOCKED_BY_RESPONSE = 'BlockedByResponse'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ErrorReason: ...

class TimeSinceEpoch(float):
    def to_json(self) -> float: ...
    @classmethod
    def from_json(cls, json: float) -> TimeSinceEpoch: ...

class MonotonicTime(float):
    def to_json(self) -> float: ...
    @classmethod
    def from_json(cls, json: float) -> MonotonicTime: ...

class Headers(dict):
    def to_json(self) -> dict: ...
    @classmethod
    def from_json(cls, json: dict) -> Headers: ...

class ConnectionType(enum.Enum):
    NONE = 'none'
    CELLULAR2G = 'cellular2g'
    CELLULAR3G = 'cellular3g'
    CELLULAR4G = 'cellular4g'
    BLUETOOTH = 'bluetooth'
    ETHERNET = 'ethernet'
    WIFI = 'wifi'
    WIMAX = 'wimax'
    OTHER = 'other'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ConnectionType: ...

class CookieSameSite(enum.Enum):
    STRICT = 'Strict'
    LAX = 'Lax'
    NONE = 'None'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CookieSameSite: ...

class CookiePriority(enum.Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CookiePriority: ...

class CookieSourceScheme(enum.Enum):
    UNSET = 'Unset'
    NON_SECURE = 'NonSecure'
    SECURE = 'Secure'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CookieSourceScheme: ...

@dataclass
class ResourceTiming:
    request_time: float
    proxy_start: float
    proxy_end: float
    dns_start: float
    dns_end: float
    connect_start: float
    connect_end: float
    ssl_start: float
    ssl_end: float
    worker_start: float
    worker_ready: float
    worker_fetch_start: float
    worker_respond_with_settled: float
    send_start: float
    send_end: float
    push_start: float
    push_end: float
    receive_headers_start: float
    receive_headers_end: float
    worker_router_evaluation_start: float | None = ...
    worker_cache_lookup_start: float | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ResourceTiming: ...

class ResourcePriority(enum.Enum):
    VERY_LOW = 'VeryLow'
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    VERY_HIGH = 'VeryHigh'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ResourcePriority: ...

@dataclass
class PostDataEntry:
    bytes_: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PostDataEntry: ...

@dataclass
class Request:
    url: str
    method: str
    headers: Headers
    initial_priority: ResourcePriority
    referrer_policy: str
    url_fragment: str | None = ...
    post_data: str | None = ...
    has_post_data: bool | None = ...
    post_data_entries: list[PostDataEntry] | None = ...
    mixed_content_type: security.MixedContentType | None = ...
    is_link_preload: bool | None = ...
    trust_token_params: TrustTokenParams | None = ...
    is_same_site: bool | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Request: ...

@dataclass
class SignedCertificateTimestamp:
    status: str
    origin: str
    log_description: str
    log_id: str
    timestamp: float
    hash_algorithm: str
    signature_algorithm: str
    signature_data: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SignedCertificateTimestamp: ...

@dataclass
class SecurityDetails:
    protocol: str
    key_exchange: str
    cipher: str
    certificate_id: security.CertificateId
    subject_name: str
    san_list: list[str]
    issuer: str
    valid_from: TimeSinceEpoch
    valid_to: TimeSinceEpoch
    signed_certificate_timestamp_list: list[SignedCertificateTimestamp]
    certificate_transparency_compliance: CertificateTransparencyCompliance
    encrypted_client_hello: bool
    key_exchange_group: str | None = ...
    mac: str | None = ...
    server_signature_algorithm: int | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SecurityDetails: ...

class CertificateTransparencyCompliance(enum.Enum):
    UNKNOWN = 'unknown'
    NOT_COMPLIANT = 'not-compliant'
    COMPLIANT = 'compliant'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CertificateTransparencyCompliance: ...

class BlockedReason(enum.Enum):
    OTHER = 'other'
    CSP = 'csp'
    MIXED_CONTENT = 'mixed-content'
    ORIGIN = 'origin'
    INSPECTOR = 'inspector'
    INTEGRITY = 'integrity'
    SUBRESOURCE_FILTER = 'subresource-filter'
    CONTENT_TYPE = 'content-type'
    COEP_FRAME_RESOURCE_NEEDS_COEP_HEADER = 'coep-frame-resource-needs-coep-header'
    COOP_SANDBOXED_IFRAME_CANNOT_NAVIGATE_TO_COOP_PAGE = 'coop-sandboxed-iframe-cannot-navigate-to-coop-page'
    CORP_NOT_SAME_ORIGIN = 'corp-not-same-origin'
    CORP_NOT_SAME_ORIGIN_AFTER_DEFAULTED_TO_SAME_ORIGIN_BY_COEP = 'corp-not-same-origin-after-defaulted-to-same-origin-by-coep'
    CORP_NOT_SAME_ORIGIN_AFTER_DEFAULTED_TO_SAME_ORIGIN_BY_DIP = 'corp-not-same-origin-after-defaulted-to-same-origin-by-dip'
    CORP_NOT_SAME_ORIGIN_AFTER_DEFAULTED_TO_SAME_ORIGIN_BY_COEP_AND_DIP = 'corp-not-same-origin-after-defaulted-to-same-origin-by-coep-and-dip'
    CORP_NOT_SAME_SITE = 'corp-not-same-site'
    SRI_MESSAGE_SIGNATURE_MISMATCH = 'sri-message-signature-mismatch'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> BlockedReason: ...

class CorsError(enum.Enum):
    DISALLOWED_BY_MODE = 'DisallowedByMode'
    INVALID_RESPONSE = 'InvalidResponse'
    WILDCARD_ORIGIN_NOT_ALLOWED = 'WildcardOriginNotAllowed'
    MISSING_ALLOW_ORIGIN_HEADER = 'MissingAllowOriginHeader'
    MULTIPLE_ALLOW_ORIGIN_VALUES = 'MultipleAllowOriginValues'
    INVALID_ALLOW_ORIGIN_VALUE = 'InvalidAllowOriginValue'
    ALLOW_ORIGIN_MISMATCH = 'AllowOriginMismatch'
    INVALID_ALLOW_CREDENTIALS = 'InvalidAllowCredentials'
    CORS_DISABLED_SCHEME = 'CorsDisabledScheme'
    PREFLIGHT_INVALID_STATUS = 'PreflightInvalidStatus'
    PREFLIGHT_DISALLOWED_REDIRECT = 'PreflightDisallowedRedirect'
    PREFLIGHT_WILDCARD_ORIGIN_NOT_ALLOWED = 'PreflightWildcardOriginNotAllowed'
    PREFLIGHT_MISSING_ALLOW_ORIGIN_HEADER = 'PreflightMissingAllowOriginHeader'
    PREFLIGHT_MULTIPLE_ALLOW_ORIGIN_VALUES = 'PreflightMultipleAllowOriginValues'
    PREFLIGHT_INVALID_ALLOW_ORIGIN_VALUE = 'PreflightInvalidAllowOriginValue'
    PREFLIGHT_ALLOW_ORIGIN_MISMATCH = 'PreflightAllowOriginMismatch'
    PREFLIGHT_INVALID_ALLOW_CREDENTIALS = 'PreflightInvalidAllowCredentials'
    PREFLIGHT_MISSING_ALLOW_EXTERNAL = 'PreflightMissingAllowExternal'
    PREFLIGHT_INVALID_ALLOW_EXTERNAL = 'PreflightInvalidAllowExternal'
    PREFLIGHT_MISSING_ALLOW_PRIVATE_NETWORK = 'PreflightMissingAllowPrivateNetwork'
    PREFLIGHT_INVALID_ALLOW_PRIVATE_NETWORK = 'PreflightInvalidAllowPrivateNetwork'
    INVALID_ALLOW_METHODS_PREFLIGHT_RESPONSE = 'InvalidAllowMethodsPreflightResponse'
    INVALID_ALLOW_HEADERS_PREFLIGHT_RESPONSE = 'InvalidAllowHeadersPreflightResponse'
    METHOD_DISALLOWED_BY_PREFLIGHT_RESPONSE = 'MethodDisallowedByPreflightResponse'
    HEADER_DISALLOWED_BY_PREFLIGHT_RESPONSE = 'HeaderDisallowedByPreflightResponse'
    REDIRECT_CONTAINS_CREDENTIALS = 'RedirectContainsCredentials'
    INSECURE_PRIVATE_NETWORK = 'InsecurePrivateNetwork'
    INVALID_PRIVATE_NETWORK_ACCESS = 'InvalidPrivateNetworkAccess'
    UNEXPECTED_PRIVATE_NETWORK_ACCESS = 'UnexpectedPrivateNetworkAccess'
    NO_CORS_REDIRECT_MODE_NOT_FOLLOW = 'NoCorsRedirectModeNotFollow'
    PREFLIGHT_MISSING_PRIVATE_NETWORK_ACCESS_ID = 'PreflightMissingPrivateNetworkAccessId'
    PREFLIGHT_MISSING_PRIVATE_NETWORK_ACCESS_NAME = 'PreflightMissingPrivateNetworkAccessName'
    PRIVATE_NETWORK_ACCESS_PERMISSION_UNAVAILABLE = 'PrivateNetworkAccessPermissionUnavailable'
    PRIVATE_NETWORK_ACCESS_PERMISSION_DENIED = 'PrivateNetworkAccessPermissionDenied'
    LOCAL_NETWORK_ACCESS_PERMISSION_DENIED = 'LocalNetworkAccessPermissionDenied'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CorsError: ...

@dataclass
class CorsErrorStatus:
    cors_error: CorsError
    failed_parameter: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CorsErrorStatus: ...

class ServiceWorkerResponseSource(enum.Enum):
    CACHE_STORAGE = 'cache-storage'
    HTTP_CACHE = 'http-cache'
    FALLBACK_CODE = 'fallback-code'
    NETWORK = 'network'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ServiceWorkerResponseSource: ...

@dataclass
class TrustTokenParams:
    operation: TrustTokenOperationType
    refresh_policy: str
    issuers: list[str] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TrustTokenParams: ...

class TrustTokenOperationType(enum.Enum):
    ISSUANCE = 'Issuance'
    REDEMPTION = 'Redemption'
    SIGNING = 'Signing'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> TrustTokenOperationType: ...

class AlternateProtocolUsage(enum.Enum):
    ALTERNATIVE_JOB_WON_WITHOUT_RACE = 'alternativeJobWonWithoutRace'
    ALTERNATIVE_JOB_WON_RACE = 'alternativeJobWonRace'
    MAIN_JOB_WON_RACE = 'mainJobWonRace'
    MAPPING_MISSING = 'mappingMissing'
    BROKEN = 'broken'
    DNS_ALPN_H3_JOB_WON_WITHOUT_RACE = 'dnsAlpnH3JobWonWithoutRace'
    DNS_ALPN_H3_JOB_WON_RACE = 'dnsAlpnH3JobWonRace'
    UNSPECIFIED_REASON = 'unspecifiedReason'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AlternateProtocolUsage: ...

class ServiceWorkerRouterSource(enum.Enum):
    NETWORK = 'network'
    CACHE = 'cache'
    FETCH_EVENT = 'fetch-event'
    RACE_NETWORK_AND_FETCH_HANDLER = 'race-network-and-fetch-handler'
    RACE_NETWORK_AND_CACHE = 'race-network-and-cache'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ServiceWorkerRouterSource: ...

@dataclass
class ServiceWorkerRouterInfo:
    rule_id_matched: int | None = ...
    matched_source_type: ServiceWorkerRouterSource | None = ...
    actual_source_type: ServiceWorkerRouterSource | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ServiceWorkerRouterInfo: ...

@dataclass
class Response:
    url: str
    status: int
    status_text: str
    headers: Headers
    mime_type: str
    charset: str
    connection_reused: bool
    connection_id: float
    encoded_data_length: float
    security_state: security.SecurityState
    headers_text: str | None = ...
    request_headers: Headers | None = ...
    request_headers_text: str | None = ...
    remote_ip_address: str | None = ...
    remote_port: int | None = ...
    from_disk_cache: bool | None = ...
    from_service_worker: bool | None = ...
    from_prefetch_cache: bool | None = ...
    from_early_hints: bool | None = ...
    service_worker_router_info: ServiceWorkerRouterInfo | None = ...
    timing: ResourceTiming | None = ...
    service_worker_response_source: ServiceWorkerResponseSource | None = ...
    response_time: TimeSinceEpoch | None = ...
    cache_storage_cache_name: str | None = ...
    protocol: str | None = ...
    alternate_protocol_usage: AlternateProtocolUsage | None = ...
    security_details: SecurityDetails | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Response: ...

@dataclass
class WebSocketRequest:
    headers: Headers
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebSocketRequest: ...

@dataclass
class WebSocketResponse:
    status: int
    status_text: str
    headers: Headers
    headers_text: str | None = ...
    request_headers: Headers | None = ...
    request_headers_text: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebSocketResponse: ...

@dataclass
class WebSocketFrame:
    opcode: float
    mask: bool
    payload_data: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebSocketFrame: ...

@dataclass
class CachedResource:
    url: str
    type_: ResourceType
    body_size: float
    response: Response | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CachedResource: ...

@dataclass
class Initiator:
    type_: str
    stack: runtime.StackTrace | None = ...
    url: str | None = ...
    line_number: float | None = ...
    column_number: float | None = ...
    request_id: RequestId | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Initiator: ...

@dataclass
class CookiePartitionKey:
    top_level_site: str
    has_cross_site_ancestor: bool
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CookiePartitionKey: ...

@dataclass
class Cookie:
    name: str
    value: str
    domain: str
    path: str
    size: int
    http_only: bool
    secure: bool
    session: bool
    priority: CookiePriority
    same_party: bool
    source_scheme: CookieSourceScheme
    source_port: int
    expires: float | None = ...
    same_site: CookieSameSite | None = ...
    partition_key: CookiePartitionKey | None = ...
    partition_key_opaque: bool | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Cookie: ...

class SetCookieBlockedReason(enum.Enum):
    SECURE_ONLY = 'SecureOnly'
    SAME_SITE_STRICT = 'SameSiteStrict'
    SAME_SITE_LAX = 'SameSiteLax'
    SAME_SITE_UNSPECIFIED_TREATED_AS_LAX = 'SameSiteUnspecifiedTreatedAsLax'
    SAME_SITE_NONE_INSECURE = 'SameSiteNoneInsecure'
    USER_PREFERENCES = 'UserPreferences'
    THIRD_PARTY_PHASEOUT = 'ThirdPartyPhaseout'
    THIRD_PARTY_BLOCKED_IN_FIRST_PARTY_SET = 'ThirdPartyBlockedInFirstPartySet'
    SYNTAX_ERROR = 'SyntaxError'
    SCHEME_NOT_SUPPORTED = 'SchemeNotSupported'
    OVERWRITE_SECURE = 'OverwriteSecure'
    INVALID_DOMAIN = 'InvalidDomain'
    INVALID_PREFIX = 'InvalidPrefix'
    UNKNOWN_ERROR = 'UnknownError'
    SCHEMEFUL_SAME_SITE_STRICT = 'SchemefulSameSiteStrict'
    SCHEMEFUL_SAME_SITE_LAX = 'SchemefulSameSiteLax'
    SCHEMEFUL_SAME_SITE_UNSPECIFIED_TREATED_AS_LAX = 'SchemefulSameSiteUnspecifiedTreatedAsLax'
    SAME_PARTY_FROM_CROSS_PARTY_CONTEXT = 'SamePartyFromCrossPartyContext'
    SAME_PARTY_CONFLICTS_WITH_OTHER_ATTRIBUTES = 'SamePartyConflictsWithOtherAttributes'
    NAME_VALUE_PAIR_EXCEEDS_MAX_SIZE = 'NameValuePairExceedsMaxSize'
    DISALLOWED_CHARACTER = 'DisallowedCharacter'
    NO_COOKIE_CONTENT = 'NoCookieContent'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SetCookieBlockedReason: ...

class CookieBlockedReason(enum.Enum):
    SECURE_ONLY = 'SecureOnly'
    NOT_ON_PATH = 'NotOnPath'
    DOMAIN_MISMATCH = 'DomainMismatch'
    SAME_SITE_STRICT = 'SameSiteStrict'
    SAME_SITE_LAX = 'SameSiteLax'
    SAME_SITE_UNSPECIFIED_TREATED_AS_LAX = 'SameSiteUnspecifiedTreatedAsLax'
    SAME_SITE_NONE_INSECURE = 'SameSiteNoneInsecure'
    USER_PREFERENCES = 'UserPreferences'
    THIRD_PARTY_PHASEOUT = 'ThirdPartyPhaseout'
    THIRD_PARTY_BLOCKED_IN_FIRST_PARTY_SET = 'ThirdPartyBlockedInFirstPartySet'
    UNKNOWN_ERROR = 'UnknownError'
    SCHEMEFUL_SAME_SITE_STRICT = 'SchemefulSameSiteStrict'
    SCHEMEFUL_SAME_SITE_LAX = 'SchemefulSameSiteLax'
    SCHEMEFUL_SAME_SITE_UNSPECIFIED_TREATED_AS_LAX = 'SchemefulSameSiteUnspecifiedTreatedAsLax'
    SAME_PARTY_FROM_CROSS_PARTY_CONTEXT = 'SamePartyFromCrossPartyContext'
    NAME_VALUE_PAIR_EXCEEDS_MAX_SIZE = 'NameValuePairExceedsMaxSize'
    PORT_MISMATCH = 'PortMismatch'
    SCHEME_MISMATCH = 'SchemeMismatch'
    ANONYMOUS_CONTEXT = 'AnonymousContext'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CookieBlockedReason: ...

class CookieExemptionReason(enum.Enum):
    NONE = 'None'
    USER_SETTING = 'UserSetting'
    TPCD_METADATA = 'TPCDMetadata'
    TPCD_DEPRECATION_TRIAL = 'TPCDDeprecationTrial'
    TOP_LEVEL_TPCD_DEPRECATION_TRIAL = 'TopLevelTPCDDeprecationTrial'
    TPCD_HEURISTICS = 'TPCDHeuristics'
    ENTERPRISE_POLICY = 'EnterprisePolicy'
    STORAGE_ACCESS = 'StorageAccess'
    TOP_LEVEL_STORAGE_ACCESS = 'TopLevelStorageAccess'
    SCHEME = 'Scheme'
    SAME_SITE_NONE_COOKIES_IN_SANDBOX = 'SameSiteNoneCookiesInSandbox'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CookieExemptionReason: ...

@dataclass
class BlockedSetCookieWithReason:
    blocked_reasons: list[SetCookieBlockedReason]
    cookie_line: str
    cookie: Cookie | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BlockedSetCookieWithReason: ...

@dataclass
class ExemptedSetCookieWithReason:
    exemption_reason: CookieExemptionReason
    cookie_line: str
    cookie: Cookie
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ExemptedSetCookieWithReason: ...

@dataclass
class AssociatedCookie:
    cookie: Cookie
    blocked_reasons: list[CookieBlockedReason]
    exemption_reason: CookieExemptionReason | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AssociatedCookie: ...

@dataclass
class CookieParam:
    name: str
    value: str
    url: str | None = ...
    domain: str | None = ...
    path: str | None = ...
    secure: bool | None = ...
    http_only: bool | None = ...
    same_site: CookieSameSite | None = ...
    expires: TimeSinceEpoch | None = ...
    priority: CookiePriority | None = ...
    same_party: bool | None = ...
    source_scheme: CookieSourceScheme | None = ...
    source_port: int | None = ...
    partition_key: CookiePartitionKey | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CookieParam: ...

@dataclass
class AuthChallenge:
    origin: str
    scheme: str
    realm: str
    source: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AuthChallenge: ...

@dataclass
class AuthChallengeResponse:
    response: str
    username: str | None = ...
    password: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AuthChallengeResponse: ...

class InterceptionStage(enum.Enum):
    REQUEST = 'Request'
    HEADERS_RECEIVED = 'HeadersReceived'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> InterceptionStage: ...

@dataclass
class RequestPattern:
    url_pattern: str | None = ...
    resource_type: ResourceType | None = ...
    interception_stage: InterceptionStage | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RequestPattern: ...

@dataclass
class SignedExchangeSignature:
    label: str
    signature: str
    integrity: str
    validity_url: str
    date: int
    expires: int
    cert_url: str | None = ...
    cert_sha256: str | None = ...
    certificates: list[str] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SignedExchangeSignature: ...

@dataclass
class SignedExchangeHeader:
    request_url: str
    response_code: int
    response_headers: Headers
    signatures: list[SignedExchangeSignature]
    header_integrity: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SignedExchangeHeader: ...

class SignedExchangeErrorField(enum.Enum):
    SIGNATURE_SIG = 'signatureSig'
    SIGNATURE_INTEGRITY = 'signatureIntegrity'
    SIGNATURE_CERT_URL = 'signatureCertUrl'
    SIGNATURE_CERT_SHA256 = 'signatureCertSha256'
    SIGNATURE_VALIDITY_URL = 'signatureValidityUrl'
    SIGNATURE_TIMESTAMPS = 'signatureTimestamps'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SignedExchangeErrorField: ...

@dataclass
class SignedExchangeError:
    message: str
    signature_index: int | None = ...
    error_field: SignedExchangeErrorField | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SignedExchangeError: ...

@dataclass
class SignedExchangeInfo:
    outer_response: Response
    has_extra_info: bool
    header: SignedExchangeHeader | None = ...
    security_details: SecurityDetails | None = ...
    errors: list[SignedExchangeError] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SignedExchangeInfo: ...

class ContentEncoding(enum.Enum):
    DEFLATE = 'deflate'
    GZIP = 'gzip'
    BR = 'br'
    ZSTD = 'zstd'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ContentEncoding: ...

class DirectSocketDnsQueryType(enum.Enum):
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> DirectSocketDnsQueryType: ...

@dataclass
class DirectTCPSocketOptions:
    no_delay: bool
    keep_alive_delay: float | None = ...
    send_buffer_size: float | None = ...
    receive_buffer_size: float | None = ...
    dns_query_type: DirectSocketDnsQueryType | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectTCPSocketOptions: ...

@dataclass
class DirectUDPSocketOptions:
    remote_addr: str | None = ...
    remote_port: int | None = ...
    local_addr: str | None = ...
    local_port: int | None = ...
    dns_query_type: DirectSocketDnsQueryType | None = ...
    send_buffer_size: float | None = ...
    receive_buffer_size: float | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectUDPSocketOptions: ...

@dataclass
class DirectUDPMessage:
    data: str
    remote_addr: str | None = ...
    remote_port: int | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectUDPMessage: ...

class PrivateNetworkRequestPolicy(enum.Enum):
    ALLOW = 'Allow'
    BLOCK_FROM_INSECURE_TO_MORE_PRIVATE = 'BlockFromInsecureToMorePrivate'
    WARN_FROM_INSECURE_TO_MORE_PRIVATE = 'WarnFromInsecureToMorePrivate'
    PREFLIGHT_BLOCK = 'PreflightBlock'
    PREFLIGHT_WARN = 'PreflightWarn'
    PERMISSION_BLOCK = 'PermissionBlock'
    PERMISSION_WARN = 'PermissionWarn'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PrivateNetworkRequestPolicy: ...

class IPAddressSpace(enum.Enum):
    LOOPBACK = 'Loopback'
    LOCAL = 'Local'
    PUBLIC = 'Public'
    UNKNOWN = 'Unknown'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> IPAddressSpace: ...

@dataclass
class ConnectTiming:
    request_time: float
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ConnectTiming: ...

@dataclass
class ClientSecurityState:
    initiator_is_secure_context: bool
    initiator_ip_address_space: IPAddressSpace
    private_network_request_policy: PrivateNetworkRequestPolicy
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ClientSecurityState: ...

class CrossOriginOpenerPolicyValue(enum.Enum):
    SAME_ORIGIN = 'SameOrigin'
    SAME_ORIGIN_ALLOW_POPUPS = 'SameOriginAllowPopups'
    RESTRICT_PROPERTIES = 'RestrictProperties'
    UNSAFE_NONE = 'UnsafeNone'
    SAME_ORIGIN_PLUS_COEP = 'SameOriginPlusCoep'
    RESTRICT_PROPERTIES_PLUS_COEP = 'RestrictPropertiesPlusCoep'
    NOOPENER_ALLOW_POPUPS = 'NoopenerAllowPopups'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CrossOriginOpenerPolicyValue: ...

@dataclass
class CrossOriginOpenerPolicyStatus:
    value: CrossOriginOpenerPolicyValue
    report_only_value: CrossOriginOpenerPolicyValue
    reporting_endpoint: str | None = ...
    report_only_reporting_endpoint: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CrossOriginOpenerPolicyStatus: ...

class CrossOriginEmbedderPolicyValue(enum.Enum):
    NONE = 'None'
    CREDENTIALLESS = 'Credentialless'
    REQUIRE_CORP = 'RequireCorp'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CrossOriginEmbedderPolicyValue: ...

@dataclass
class CrossOriginEmbedderPolicyStatus:
    value: CrossOriginEmbedderPolicyValue
    report_only_value: CrossOriginEmbedderPolicyValue
    reporting_endpoint: str | None = ...
    report_only_reporting_endpoint: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CrossOriginEmbedderPolicyStatus: ...

class ContentSecurityPolicySource(enum.Enum):
    HTTP = 'HTTP'
    META = 'Meta'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ContentSecurityPolicySource: ...

@dataclass
class ContentSecurityPolicyStatus:
    effective_directives: str
    is_enforced: bool
    source: ContentSecurityPolicySource
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ContentSecurityPolicyStatus: ...

@dataclass
class SecurityIsolationStatus:
    coop: CrossOriginOpenerPolicyStatus | None = ...
    coep: CrossOriginEmbedderPolicyStatus | None = ...
    csp: list[ContentSecurityPolicyStatus] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SecurityIsolationStatus: ...

class ReportStatus(enum.Enum):
    QUEUED = 'Queued'
    PENDING = 'Pending'
    MARKED_FOR_REMOVAL = 'MarkedForRemoval'
    SUCCESS = 'Success'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ReportStatus: ...

class ReportId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ReportId: ...

@dataclass
class ReportingApiReport:
    id_: ReportId
    initiator_url: str
    destination: str
    type_: str
    timestamp: TimeSinceEpoch
    depth: int
    completed_attempts: int
    body: dict
    status: ReportStatus
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ReportingApiReport: ...

@dataclass
class ReportingApiEndpoint:
    url: str
    group_name: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ReportingApiEndpoint: ...

@dataclass
class LoadNetworkResourcePageResult:
    success: bool
    net_error: float | None = ...
    net_error_name: str | None = ...
    http_status_code: float | None = ...
    stream: io.StreamHandle | None = ...
    headers: Headers | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LoadNetworkResourcePageResult: ...

@dataclass
class LoadNetworkResourceOptions:
    disable_cache: bool
    include_credentials: bool
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LoadNetworkResourceOptions: ...

def set_accepted_encodings(encodings: list[ContentEncoding]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_accepted_encodings_override() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def can_clear_browser_cache() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, bool]: ...
def can_clear_browser_cookies() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, bool]: ...
def can_emulate_network_conditions() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, bool]: ...
def clear_browser_cache() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_browser_cookies() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def continue_intercepted_request(interception_id: InterceptionId, error_reason: ErrorReason | None = None, raw_response: str | None = None, url: str | None = None, method: str | None = None, post_data: str | None = None, headers: Headers | None = None, auth_challenge_response: AuthChallengeResponse | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def delete_cookies(name: str, url: str | None = None, domain: str | None = None, path: str | None = None, partition_key: CookiePartitionKey | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def emulate_network_conditions(offline: bool, latency: float, download_throughput: float, upload_throughput: float, connection_type: ConnectionType | None = None, packet_loss: float | None = None, packet_queue_length: int | None = None, packet_reordering: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable(max_total_buffer_size: int | None = None, max_resource_buffer_size: int | None = None, max_post_data_size: int | None = None, report_direct_socket_traffic: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_all_cookies() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[Cookie]]: ...
def get_certificate(origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[str]]: ...
def get_cookies(urls: list[str] | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[Cookie]]: ...
def get_response_body(request_id: RequestId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[str, bool]]: ...
def get_request_post_data(request_id: RequestId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, str]: ...
def get_response_body_for_interception(interception_id: InterceptionId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[str, bool]]: ...
def take_response_body_for_interception_as_stream(interception_id: InterceptionId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, io.StreamHandle]: ...
def replay_xhr(request_id: RequestId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def search_in_response_body(request_id: RequestId, query: str, case_sensitive: bool | None = None, is_regex: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[debugger.SearchMatch]]: ...
def set_blocked_ur_ls(urls: list[str]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_bypass_service_worker(bypass: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_cache_disabled(cache_disabled: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_cookie(name: str, value: str, url: str | None = None, domain: str | None = None, path: str | None = None, secure: bool | None = None, http_only: bool | None = None, same_site: CookieSameSite | None = None, expires: TimeSinceEpoch | None = None, priority: CookiePriority | None = None, same_party: bool | None = None, source_scheme: CookieSourceScheme | None = None, source_port: int | None = None, partition_key: CookiePartitionKey | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, bool]: ...
def set_cookies(cookies: list[CookieParam]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_extra_http_headers(headers: Headers) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_attach_debug_stack(enabled: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_request_interception(patterns: list[RequestPattern]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_user_agent_override(user_agent: str, accept_language: str | None = None, platform: str | None = None, user_agent_metadata: emulation.UserAgentMetadata | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def stream_resource_content(request_id: RequestId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, str]: ...
def get_security_isolation_status(frame_id: page.FrameId | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, SecurityIsolationStatus]: ...
def enable_reporting_api(enable: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def load_network_resource(url: str, options: LoadNetworkResourceOptions, frame_id: page.FrameId | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, LoadNetworkResourcePageResult]: ...
def set_cookie_controls(enable_third_party_cookie_restriction: bool, disable_third_party_cookie_metadata: bool, disable_third_party_cookie_heuristics: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class DataReceived:
    request_id: RequestId
    timestamp: MonotonicTime
    data_length: int
    encoded_data_length: int
    data: str | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DataReceived: ...

@dataclass
class EventSourceMessageReceived:
    request_id: RequestId
    timestamp: MonotonicTime
    event_name: str
    event_id: str
    data: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> EventSourceMessageReceived: ...

@dataclass
class LoadingFailed:
    request_id: RequestId
    timestamp: MonotonicTime
    type_: ResourceType
    error_text: str
    canceled: bool | None
    blocked_reason: BlockedReason | None
    cors_error_status: CorsErrorStatus | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LoadingFailed: ...

@dataclass
class LoadingFinished:
    request_id: RequestId
    timestamp: MonotonicTime
    encoded_data_length: float
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LoadingFinished: ...

@dataclass
class RequestIntercepted:
    interception_id: InterceptionId
    request: Request
    frame_id: page.FrameId
    resource_type: ResourceType
    is_navigation_request: bool
    is_download: bool | None
    redirect_url: str | None
    auth_challenge: AuthChallenge | None
    response_error_reason: ErrorReason | None
    response_status_code: int | None
    response_headers: Headers | None
    request_id: RequestId | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RequestIntercepted: ...

@dataclass
class RequestServedFromCache:
    request_id: RequestId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RequestServedFromCache: ...

@dataclass
class RequestWillBeSent:
    request_id: RequestId
    loader_id: LoaderId
    document_url: str
    request: Request
    timestamp: MonotonicTime
    wall_time: TimeSinceEpoch
    initiator: Initiator
    redirect_has_extra_info: bool
    redirect_response: Response | None
    type_: ResourceType | None
    frame_id: page.FrameId | None
    has_user_gesture: bool | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RequestWillBeSent: ...

@dataclass
class ResourceChangedPriority:
    request_id: RequestId
    new_priority: ResourcePriority
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ResourceChangedPriority: ...

@dataclass
class SignedExchangeReceived:
    request_id: RequestId
    info: SignedExchangeInfo
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SignedExchangeReceived: ...

@dataclass
class ResponseReceived:
    request_id: RequestId
    loader_id: LoaderId
    timestamp: MonotonicTime
    type_: ResourceType
    response: Response
    has_extra_info: bool
    frame_id: page.FrameId | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ResponseReceived: ...

@dataclass
class WebSocketClosed:
    request_id: RequestId
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebSocketClosed: ...

@dataclass
class WebSocketCreated:
    request_id: RequestId
    url: str
    initiator: Initiator | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebSocketCreated: ...

@dataclass
class WebSocketFrameError:
    request_id: RequestId
    timestamp: MonotonicTime
    error_message: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebSocketFrameError: ...

@dataclass
class WebSocketFrameReceived:
    request_id: RequestId
    timestamp: MonotonicTime
    response: WebSocketFrame
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebSocketFrameReceived: ...

@dataclass
class WebSocketFrameSent:
    request_id: RequestId
    timestamp: MonotonicTime
    response: WebSocketFrame
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebSocketFrameSent: ...

@dataclass
class WebSocketHandshakeResponseReceived:
    request_id: RequestId
    timestamp: MonotonicTime
    response: WebSocketResponse
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebSocketHandshakeResponseReceived: ...

@dataclass
class WebSocketWillSendHandshakeRequest:
    request_id: RequestId
    timestamp: MonotonicTime
    wall_time: TimeSinceEpoch
    request: WebSocketRequest
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebSocketWillSendHandshakeRequest: ...

@dataclass
class WebTransportCreated:
    transport_id: RequestId
    url: str
    timestamp: MonotonicTime
    initiator: Initiator | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebTransportCreated: ...

@dataclass
class WebTransportConnectionEstablished:
    transport_id: RequestId
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebTransportConnectionEstablished: ...

@dataclass
class WebTransportClosed:
    transport_id: RequestId
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebTransportClosed: ...

@dataclass
class DirectTCPSocketCreated:
    identifier: RequestId
    remote_addr: str
    remote_port: int
    options: DirectTCPSocketOptions
    timestamp: MonotonicTime
    initiator: Initiator | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectTCPSocketCreated: ...

@dataclass
class DirectTCPSocketOpened:
    identifier: RequestId
    remote_addr: str
    remote_port: int
    timestamp: MonotonicTime
    local_addr: str | None
    local_port: int | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectTCPSocketOpened: ...

@dataclass
class DirectTCPSocketAborted:
    identifier: RequestId
    error_message: str
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectTCPSocketAborted: ...

@dataclass
class DirectTCPSocketClosed:
    identifier: RequestId
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectTCPSocketClosed: ...

@dataclass
class DirectTCPSocketChunkSent:
    identifier: RequestId
    data: str
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectTCPSocketChunkSent: ...

@dataclass
class DirectTCPSocketChunkReceived:
    identifier: RequestId
    data: str
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectTCPSocketChunkReceived: ...

@dataclass
class DirectUDPSocketCreated:
    identifier: RequestId
    options: DirectUDPSocketOptions
    timestamp: MonotonicTime
    initiator: Initiator | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectUDPSocketCreated: ...

@dataclass
class DirectUDPSocketOpened:
    identifier: RequestId
    local_addr: str
    local_port: int
    timestamp: MonotonicTime
    remote_addr: str | None
    remote_port: int | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectUDPSocketOpened: ...

@dataclass
class DirectUDPSocketAborted:
    identifier: RequestId
    error_message: str
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectUDPSocketAborted: ...

@dataclass
class DirectUDPSocketClosed:
    identifier: RequestId
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectUDPSocketClosed: ...

@dataclass
class DirectUDPSocketChunkSent:
    identifier: RequestId
    message: DirectUDPMessage
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectUDPSocketChunkSent: ...

@dataclass
class DirectUDPSocketChunkReceived:
    identifier: RequestId
    message: DirectUDPMessage
    timestamp: MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DirectUDPSocketChunkReceived: ...

@dataclass
class RequestWillBeSentExtraInfo:
    request_id: RequestId
    associated_cookies: list[AssociatedCookie]
    headers: Headers
    connect_timing: ConnectTiming
    client_security_state: ClientSecurityState | None
    site_has_cookie_in_other_partition: bool | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RequestWillBeSentExtraInfo: ...

@dataclass
class ResponseReceivedExtraInfo:
    request_id: RequestId
    blocked_cookies: list[BlockedSetCookieWithReason]
    headers: Headers
    resource_ip_address_space: IPAddressSpace
    status_code: int
    headers_text: str | None
    cookie_partition_key: CookiePartitionKey | None
    cookie_partition_key_opaque: bool | None
    exempted_cookies: list[ExemptedSetCookieWithReason] | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ResponseReceivedExtraInfo: ...

@dataclass
class ResponseReceivedEarlyHints:
    request_id: RequestId
    headers: Headers
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ResponseReceivedEarlyHints: ...

@dataclass
class TrustTokenOperationDone:
    status: str
    type_: TrustTokenOperationType
    request_id: RequestId
    top_level_origin: str | None
    issuer_origin: str | None
    issued_token_count: int | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TrustTokenOperationDone: ...

@dataclass
class PolicyUpdated:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PolicyUpdated: ...

@dataclass
class SubresourceWebBundleMetadataReceived:
    request_id: RequestId
    urls: list[str]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SubresourceWebBundleMetadataReceived: ...

@dataclass
class SubresourceWebBundleMetadataError:
    request_id: RequestId
    error_message: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SubresourceWebBundleMetadataError: ...

@dataclass
class SubresourceWebBundleInnerResponseParsed:
    inner_request_id: RequestId
    inner_request_url: str
    bundle_request_id: RequestId | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SubresourceWebBundleInnerResponseParsed: ...

@dataclass
class SubresourceWebBundleInnerResponseError:
    inner_request_id: RequestId
    inner_request_url: str
    error_message: str
    bundle_request_id: RequestId | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SubresourceWebBundleInnerResponseError: ...

@dataclass
class ReportingApiReportAdded:
    report: ReportingApiReport
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ReportingApiReportAdded: ...

@dataclass
class ReportingApiReportUpdated:
    report: ReportingApiReport
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ReportingApiReportUpdated: ...

@dataclass
class ReportingApiEndpointsChangedForOrigin:
    origin: str
    endpoints: list[ReportingApiEndpoint]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ReportingApiEndpointsChangedForOrigin: ...
