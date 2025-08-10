import enum
import typing
from . import dom as dom, network as network, page as page, runtime as runtime
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

@dataclass
class AffectedCookie:
    name: str
    path: str
    domain: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AffectedCookie: ...

@dataclass
class AffectedRequest:
    url: str
    request_id: network.RequestId | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AffectedRequest: ...

@dataclass
class AffectedFrame:
    frame_id: page.FrameId
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AffectedFrame: ...

class CookieExclusionReason(enum.Enum):
    EXCLUDE_SAME_SITE_UNSPECIFIED_TREATED_AS_LAX = 'ExcludeSameSiteUnspecifiedTreatedAsLax'
    EXCLUDE_SAME_SITE_NONE_INSECURE = 'ExcludeSameSiteNoneInsecure'
    EXCLUDE_SAME_SITE_LAX = 'ExcludeSameSiteLax'
    EXCLUDE_SAME_SITE_STRICT = 'ExcludeSameSiteStrict'
    EXCLUDE_INVALID_SAME_PARTY = 'ExcludeInvalidSameParty'
    EXCLUDE_SAME_PARTY_CROSS_PARTY_CONTEXT = 'ExcludeSamePartyCrossPartyContext'
    EXCLUDE_DOMAIN_NON_ASCII = 'ExcludeDomainNonASCII'
    EXCLUDE_THIRD_PARTY_COOKIE_BLOCKED_IN_FIRST_PARTY_SET = 'ExcludeThirdPartyCookieBlockedInFirstPartySet'
    EXCLUDE_THIRD_PARTY_PHASEOUT = 'ExcludeThirdPartyPhaseout'
    EXCLUDE_PORT_MISMATCH = 'ExcludePortMismatch'
    EXCLUDE_SCHEME_MISMATCH = 'ExcludeSchemeMismatch'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CookieExclusionReason: ...

class CookieWarningReason(enum.Enum):
    WARN_SAME_SITE_UNSPECIFIED_CROSS_SITE_CONTEXT = 'WarnSameSiteUnspecifiedCrossSiteContext'
    WARN_SAME_SITE_NONE_INSECURE = 'WarnSameSiteNoneInsecure'
    WARN_SAME_SITE_UNSPECIFIED_LAX_ALLOW_UNSAFE = 'WarnSameSiteUnspecifiedLaxAllowUnsafe'
    WARN_SAME_SITE_STRICT_LAX_DOWNGRADE_STRICT = 'WarnSameSiteStrictLaxDowngradeStrict'
    WARN_SAME_SITE_STRICT_CROSS_DOWNGRADE_STRICT = 'WarnSameSiteStrictCrossDowngradeStrict'
    WARN_SAME_SITE_STRICT_CROSS_DOWNGRADE_LAX = 'WarnSameSiteStrictCrossDowngradeLax'
    WARN_SAME_SITE_LAX_CROSS_DOWNGRADE_STRICT = 'WarnSameSiteLaxCrossDowngradeStrict'
    WARN_SAME_SITE_LAX_CROSS_DOWNGRADE_LAX = 'WarnSameSiteLaxCrossDowngradeLax'
    WARN_ATTRIBUTE_VALUE_EXCEEDS_MAX_SIZE = 'WarnAttributeValueExceedsMaxSize'
    WARN_DOMAIN_NON_ASCII = 'WarnDomainNonASCII'
    WARN_THIRD_PARTY_PHASEOUT = 'WarnThirdPartyPhaseout'
    WARN_CROSS_SITE_REDIRECT_DOWNGRADE_CHANGES_INCLUSION = 'WarnCrossSiteRedirectDowngradeChangesInclusion'
    WARN_DEPRECATION_TRIAL_METADATA = 'WarnDeprecationTrialMetadata'
    WARN_THIRD_PARTY_COOKIE_HEURISTIC = 'WarnThirdPartyCookieHeuristic'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CookieWarningReason: ...

class CookieOperation(enum.Enum):
    SET_COOKIE = 'SetCookie'
    READ_COOKIE = 'ReadCookie'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CookieOperation: ...

class InsightType(enum.Enum):
    GIT_HUB_RESOURCE = 'GitHubResource'
    GRACE_PERIOD = 'GracePeriod'
    HEURISTICS = 'Heuristics'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> InsightType: ...

@dataclass
class CookieIssueInsight:
    type_: InsightType
    table_entry_url: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CookieIssueInsight: ...

@dataclass
class CookieIssueDetails:
    cookie_warning_reasons: list[CookieWarningReason]
    cookie_exclusion_reasons: list[CookieExclusionReason]
    operation: CookieOperation
    cookie: AffectedCookie | None = ...
    raw_cookie_line: str | None = ...
    site_for_cookies: str | None = ...
    cookie_url: str | None = ...
    request: AffectedRequest | None = ...
    insight: CookieIssueInsight | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CookieIssueDetails: ...

class MixedContentResolutionStatus(enum.Enum):
    MIXED_CONTENT_BLOCKED = 'MixedContentBlocked'
    MIXED_CONTENT_AUTOMATICALLY_UPGRADED = 'MixedContentAutomaticallyUpgraded'
    MIXED_CONTENT_WARNING = 'MixedContentWarning'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> MixedContentResolutionStatus: ...

class MixedContentResourceType(enum.Enum):
    ATTRIBUTION_SRC = 'AttributionSrc'
    AUDIO = 'Audio'
    BEACON = 'Beacon'
    CSP_REPORT = 'CSPReport'
    DOWNLOAD = 'Download'
    EVENT_SOURCE = 'EventSource'
    FAVICON = 'Favicon'
    FONT = 'Font'
    FORM = 'Form'
    FRAME = 'Frame'
    IMAGE = 'Image'
    IMPORT = 'Import'
    JSON = 'JSON'
    MANIFEST = 'Manifest'
    PING = 'Ping'
    PLUGIN_DATA = 'PluginData'
    PLUGIN_RESOURCE = 'PluginResource'
    PREFETCH = 'Prefetch'
    RESOURCE = 'Resource'
    SCRIPT = 'Script'
    SERVICE_WORKER = 'ServiceWorker'
    SHARED_WORKER = 'SharedWorker'
    SPECULATION_RULES = 'SpeculationRules'
    STYLESHEET = 'Stylesheet'
    TRACK = 'Track'
    VIDEO = 'Video'
    WORKER = 'Worker'
    XML_HTTP_REQUEST = 'XMLHttpRequest'
    XSLT = 'XSLT'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> MixedContentResourceType: ...

@dataclass
class MixedContentIssueDetails:
    resolution_status: MixedContentResolutionStatus
    insecure_url: str
    main_resource_url: str
    resource_type: MixedContentResourceType | None = ...
    request: AffectedRequest | None = ...
    frame: AffectedFrame | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> MixedContentIssueDetails: ...

class BlockedByResponseReason(enum.Enum):
    COEP_FRAME_RESOURCE_NEEDS_COEP_HEADER = 'CoepFrameResourceNeedsCoepHeader'
    COOP_SANDBOXED_I_FRAME_CANNOT_NAVIGATE_TO_COOP_PAGE = 'CoopSandboxedIFrameCannotNavigateToCoopPage'
    CORP_NOT_SAME_ORIGIN = 'CorpNotSameOrigin'
    CORP_NOT_SAME_ORIGIN_AFTER_DEFAULTED_TO_SAME_ORIGIN_BY_COEP = 'CorpNotSameOriginAfterDefaultedToSameOriginByCoep'
    CORP_NOT_SAME_ORIGIN_AFTER_DEFAULTED_TO_SAME_ORIGIN_BY_DIP = 'CorpNotSameOriginAfterDefaultedToSameOriginByDip'
    CORP_NOT_SAME_ORIGIN_AFTER_DEFAULTED_TO_SAME_ORIGIN_BY_COEP_AND_DIP = 'CorpNotSameOriginAfterDefaultedToSameOriginByCoepAndDip'
    CORP_NOT_SAME_SITE = 'CorpNotSameSite'
    SRI_MESSAGE_SIGNATURE_MISMATCH = 'SRIMessageSignatureMismatch'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> BlockedByResponseReason: ...

@dataclass
class BlockedByResponseIssueDetails:
    request: AffectedRequest
    reason: BlockedByResponseReason
    parent_frame: AffectedFrame | None = ...
    blocked_frame: AffectedFrame | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BlockedByResponseIssueDetails: ...

class HeavyAdResolutionStatus(enum.Enum):
    HEAVY_AD_BLOCKED = 'HeavyAdBlocked'
    HEAVY_AD_WARNING = 'HeavyAdWarning'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> HeavyAdResolutionStatus: ...

class HeavyAdReason(enum.Enum):
    NETWORK_TOTAL_LIMIT = 'NetworkTotalLimit'
    CPU_TOTAL_LIMIT = 'CpuTotalLimit'
    CPU_PEAK_LIMIT = 'CpuPeakLimit'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> HeavyAdReason: ...

@dataclass
class HeavyAdIssueDetails:
    resolution: HeavyAdResolutionStatus
    reason: HeavyAdReason
    frame: AffectedFrame
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> HeavyAdIssueDetails: ...

class ContentSecurityPolicyViolationType(enum.Enum):
    K_INLINE_VIOLATION = 'kInlineViolation'
    K_EVAL_VIOLATION = 'kEvalViolation'
    K_URL_VIOLATION = 'kURLViolation'
    K_SRI_VIOLATION = 'kSRIViolation'
    K_TRUSTED_TYPES_SINK_VIOLATION = 'kTrustedTypesSinkViolation'
    K_TRUSTED_TYPES_POLICY_VIOLATION = 'kTrustedTypesPolicyViolation'
    K_WASM_EVAL_VIOLATION = 'kWasmEvalViolation'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ContentSecurityPolicyViolationType: ...

@dataclass
class SourceCodeLocation:
    url: str
    line_number: int
    column_number: int
    script_id: runtime.ScriptId | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SourceCodeLocation: ...

@dataclass
class ContentSecurityPolicyIssueDetails:
    violated_directive: str
    is_report_only: bool
    content_security_policy_violation_type: ContentSecurityPolicyViolationType
    blocked_url: str | None = ...
    frame_ancestor: AffectedFrame | None = ...
    source_code_location: SourceCodeLocation | None = ...
    violating_node_id: dom.BackendNodeId | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ContentSecurityPolicyIssueDetails: ...

class SharedArrayBufferIssueType(enum.Enum):
    TRANSFER_ISSUE = 'TransferIssue'
    CREATION_ISSUE = 'CreationIssue'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SharedArrayBufferIssueType: ...

@dataclass
class SharedArrayBufferIssueDetails:
    source_code_location: SourceCodeLocation
    is_warning: bool
    type_: SharedArrayBufferIssueType
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SharedArrayBufferIssueDetails: ...

@dataclass
class LowTextContrastIssueDetails:
    violating_node_id: dom.BackendNodeId
    violating_node_selector: str
    contrast_ratio: float
    threshold_aa: float
    threshold_aaa: float
    font_size: str
    font_weight: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LowTextContrastIssueDetails: ...

@dataclass
class CorsIssueDetails:
    cors_error_status: network.CorsErrorStatus
    is_warning: bool
    request: AffectedRequest
    location: SourceCodeLocation | None = ...
    initiator_origin: str | None = ...
    resource_ip_address_space: network.IPAddressSpace | None = ...
    client_security_state: network.ClientSecurityState | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CorsIssueDetails: ...

class AttributionReportingIssueType(enum.Enum):
    PERMISSION_POLICY_DISABLED = 'PermissionPolicyDisabled'
    UNTRUSTWORTHY_REPORTING_ORIGIN = 'UntrustworthyReportingOrigin'
    INSECURE_CONTEXT = 'InsecureContext'
    INVALID_HEADER = 'InvalidHeader'
    INVALID_REGISTER_TRIGGER_HEADER = 'InvalidRegisterTriggerHeader'
    SOURCE_AND_TRIGGER_HEADERS = 'SourceAndTriggerHeaders'
    SOURCE_IGNORED = 'SourceIgnored'
    TRIGGER_IGNORED = 'TriggerIgnored'
    OS_SOURCE_IGNORED = 'OsSourceIgnored'
    OS_TRIGGER_IGNORED = 'OsTriggerIgnored'
    INVALID_REGISTER_OS_SOURCE_HEADER = 'InvalidRegisterOsSourceHeader'
    INVALID_REGISTER_OS_TRIGGER_HEADER = 'InvalidRegisterOsTriggerHeader'
    WEB_AND_OS_HEADERS = 'WebAndOsHeaders'
    NO_WEB_OR_OS_SUPPORT = 'NoWebOrOsSupport'
    NAVIGATION_REGISTRATION_WITHOUT_TRANSIENT_USER_ACTIVATION = 'NavigationRegistrationWithoutTransientUserActivation'
    INVALID_INFO_HEADER = 'InvalidInfoHeader'
    NO_REGISTER_SOURCE_HEADER = 'NoRegisterSourceHeader'
    NO_REGISTER_TRIGGER_HEADER = 'NoRegisterTriggerHeader'
    NO_REGISTER_OS_SOURCE_HEADER = 'NoRegisterOsSourceHeader'
    NO_REGISTER_OS_TRIGGER_HEADER = 'NoRegisterOsTriggerHeader'
    NAVIGATION_REGISTRATION_UNIQUE_SCOPE_ALREADY_SET = 'NavigationRegistrationUniqueScopeAlreadySet'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AttributionReportingIssueType: ...

class SharedDictionaryError(enum.Enum):
    USE_ERROR_CROSS_ORIGIN_NO_CORS_REQUEST = 'UseErrorCrossOriginNoCorsRequest'
    USE_ERROR_DICTIONARY_LOAD_FAILURE = 'UseErrorDictionaryLoadFailure'
    USE_ERROR_MATCHING_DICTIONARY_NOT_USED = 'UseErrorMatchingDictionaryNotUsed'
    USE_ERROR_UNEXPECTED_CONTENT_DICTIONARY_HEADER = 'UseErrorUnexpectedContentDictionaryHeader'
    WRITE_ERROR_COSS_ORIGIN_NO_CORS_REQUEST = 'WriteErrorCossOriginNoCorsRequest'
    WRITE_ERROR_DISALLOWED_BY_SETTINGS = 'WriteErrorDisallowedBySettings'
    WRITE_ERROR_EXPIRED_RESPONSE = 'WriteErrorExpiredResponse'
    WRITE_ERROR_FEATURE_DISABLED = 'WriteErrorFeatureDisabled'
    WRITE_ERROR_INSUFFICIENT_RESOURCES = 'WriteErrorInsufficientResources'
    WRITE_ERROR_INVALID_MATCH_FIELD = 'WriteErrorInvalidMatchField'
    WRITE_ERROR_INVALID_STRUCTURED_HEADER = 'WriteErrorInvalidStructuredHeader'
    WRITE_ERROR_NAVIGATION_REQUEST = 'WriteErrorNavigationRequest'
    WRITE_ERROR_NO_MATCH_FIELD = 'WriteErrorNoMatchField'
    WRITE_ERROR_NON_LIST_MATCH_DEST_FIELD = 'WriteErrorNonListMatchDestField'
    WRITE_ERROR_NON_SECURE_CONTEXT = 'WriteErrorNonSecureContext'
    WRITE_ERROR_NON_STRING_ID_FIELD = 'WriteErrorNonStringIdField'
    WRITE_ERROR_NON_STRING_IN_MATCH_DEST_LIST = 'WriteErrorNonStringInMatchDestList'
    WRITE_ERROR_NON_STRING_MATCH_FIELD = 'WriteErrorNonStringMatchField'
    WRITE_ERROR_NON_TOKEN_TYPE_FIELD = 'WriteErrorNonTokenTypeField'
    WRITE_ERROR_REQUEST_ABORTED = 'WriteErrorRequestAborted'
    WRITE_ERROR_SHUTTING_DOWN = 'WriteErrorShuttingDown'
    WRITE_ERROR_TOO_LONG_ID_FIELD = 'WriteErrorTooLongIdField'
    WRITE_ERROR_UNSUPPORTED_TYPE = 'WriteErrorUnsupportedType'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SharedDictionaryError: ...

class SRIMessageSignatureError(enum.Enum):
    MISSING_SIGNATURE_HEADER = 'MissingSignatureHeader'
    MISSING_SIGNATURE_INPUT_HEADER = 'MissingSignatureInputHeader'
    INVALID_SIGNATURE_HEADER = 'InvalidSignatureHeader'
    INVALID_SIGNATURE_INPUT_HEADER = 'InvalidSignatureInputHeader'
    SIGNATURE_HEADER_VALUE_IS_NOT_BYTE_SEQUENCE = 'SignatureHeaderValueIsNotByteSequence'
    SIGNATURE_HEADER_VALUE_IS_PARAMETERIZED = 'SignatureHeaderValueIsParameterized'
    SIGNATURE_HEADER_VALUE_IS_INCORRECT_LENGTH = 'SignatureHeaderValueIsIncorrectLength'
    SIGNATURE_INPUT_HEADER_MISSING_LABEL = 'SignatureInputHeaderMissingLabel'
    SIGNATURE_INPUT_HEADER_VALUE_NOT_INNER_LIST = 'SignatureInputHeaderValueNotInnerList'
    SIGNATURE_INPUT_HEADER_VALUE_MISSING_COMPONENTS = 'SignatureInputHeaderValueMissingComponents'
    SIGNATURE_INPUT_HEADER_INVALID_COMPONENT_TYPE = 'SignatureInputHeaderInvalidComponentType'
    SIGNATURE_INPUT_HEADER_INVALID_COMPONENT_NAME = 'SignatureInputHeaderInvalidComponentName'
    SIGNATURE_INPUT_HEADER_INVALID_HEADER_COMPONENT_PARAMETER = 'SignatureInputHeaderInvalidHeaderComponentParameter'
    SIGNATURE_INPUT_HEADER_INVALID_DERIVED_COMPONENT_PARAMETER = 'SignatureInputHeaderInvalidDerivedComponentParameter'
    SIGNATURE_INPUT_HEADER_KEY_ID_LENGTH = 'SignatureInputHeaderKeyIdLength'
    SIGNATURE_INPUT_HEADER_INVALID_PARAMETER = 'SignatureInputHeaderInvalidParameter'
    SIGNATURE_INPUT_HEADER_MISSING_REQUIRED_PARAMETERS = 'SignatureInputHeaderMissingRequiredParameters'
    VALIDATION_FAILED_SIGNATURE_EXPIRED = 'ValidationFailedSignatureExpired'
    VALIDATION_FAILED_INVALID_LENGTH = 'ValidationFailedInvalidLength'
    VALIDATION_FAILED_SIGNATURE_MISMATCH = 'ValidationFailedSignatureMismatch'
    VALIDATION_FAILED_INTEGRITY_MISMATCH = 'ValidationFailedIntegrityMismatch'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SRIMessageSignatureError: ...

@dataclass
class AttributionReportingIssueDetails:
    violation_type: AttributionReportingIssueType
    request: AffectedRequest | None = ...
    violating_node_id: dom.BackendNodeId | None = ...
    invalid_parameter: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingIssueDetails: ...

@dataclass
class QuirksModeIssueDetails:
    is_limited_quirks_mode: bool
    document_node_id: dom.BackendNodeId
    url: str
    frame_id: page.FrameId
    loader_id: network.LoaderId
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> QuirksModeIssueDetails: ...

@dataclass
class NavigatorUserAgentIssueDetails:
    url: str
    location: SourceCodeLocation | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> NavigatorUserAgentIssueDetails: ...

@dataclass
class SharedDictionaryIssueDetails:
    shared_dictionary_error: SharedDictionaryError
    request: AffectedRequest
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SharedDictionaryIssueDetails: ...

@dataclass
class SRIMessageSignatureIssueDetails:
    error: SRIMessageSignatureError
    signature_base: str
    integrity_assertions: list[str]
    request: AffectedRequest
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SRIMessageSignatureIssueDetails: ...

class GenericIssueErrorType(enum.Enum):
    FORM_LABEL_FOR_NAME_ERROR = 'FormLabelForNameError'
    FORM_DUPLICATE_ID_FOR_INPUT_ERROR = 'FormDuplicateIdForInputError'
    FORM_INPUT_WITH_NO_LABEL_ERROR = 'FormInputWithNoLabelError'
    FORM_AUTOCOMPLETE_ATTRIBUTE_EMPTY_ERROR = 'FormAutocompleteAttributeEmptyError'
    FORM_EMPTY_ID_AND_NAME_ATTRIBUTES_FOR_INPUT_ERROR = 'FormEmptyIdAndNameAttributesForInputError'
    FORM_ARIA_LABELLED_BY_TO_NON_EXISTING_ID = 'FormAriaLabelledByToNonExistingId'
    FORM_INPUT_ASSIGNED_AUTOCOMPLETE_VALUE_TO_ID_OR_NAME_ATTRIBUTE_ERROR = 'FormInputAssignedAutocompleteValueToIdOrNameAttributeError'
    FORM_LABEL_HAS_NEITHER_FOR_NOR_NESTED_INPUT = 'FormLabelHasNeitherForNorNestedInput'
    FORM_LABEL_FOR_MATCHES_NON_EXISTING_ID_ERROR = 'FormLabelForMatchesNonExistingIdError'
    FORM_INPUT_HAS_WRONG_BUT_WELL_INTENDED_AUTOCOMPLETE_VALUE_ERROR = 'FormInputHasWrongButWellIntendedAutocompleteValueError'
    RESPONSE_WAS_BLOCKED_BY_ORB = 'ResponseWasBlockedByORB'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> GenericIssueErrorType: ...

@dataclass
class GenericIssueDetails:
    error_type: GenericIssueErrorType
    frame_id: page.FrameId | None = ...
    violating_node_id: dom.BackendNodeId | None = ...
    violating_node_attribute: str | None = ...
    request: AffectedRequest | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> GenericIssueDetails: ...

@dataclass
class DeprecationIssueDetails:
    source_code_location: SourceCodeLocation
    type_: str
    affected_frame: AffectedFrame | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DeprecationIssueDetails: ...

@dataclass
class BounceTrackingIssueDetails:
    tracking_sites: list[str]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BounceTrackingIssueDetails: ...

@dataclass
class CookieDeprecationMetadataIssueDetails:
    allowed_sites: list[str]
    opt_out_percentage: float
    is_opt_out_top_level: bool
    operation: CookieOperation
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CookieDeprecationMetadataIssueDetails: ...

class ClientHintIssueReason(enum.Enum):
    META_TAG_ALLOW_LIST_INVALID_ORIGIN = 'MetaTagAllowListInvalidOrigin'
    META_TAG_MODIFIED_HTML = 'MetaTagModifiedHTML'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ClientHintIssueReason: ...

@dataclass
class FederatedAuthRequestIssueDetails:
    federated_auth_request_issue_reason: FederatedAuthRequestIssueReason
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FederatedAuthRequestIssueDetails: ...

class FederatedAuthRequestIssueReason(enum.Enum):
    SHOULD_EMBARGO = 'ShouldEmbargo'
    TOO_MANY_REQUESTS = 'TooManyRequests'
    WELL_KNOWN_HTTP_NOT_FOUND = 'WellKnownHttpNotFound'
    WELL_KNOWN_NO_RESPONSE = 'WellKnownNoResponse'
    WELL_KNOWN_INVALID_RESPONSE = 'WellKnownInvalidResponse'
    WELL_KNOWN_LIST_EMPTY = 'WellKnownListEmpty'
    WELL_KNOWN_INVALID_CONTENT_TYPE = 'WellKnownInvalidContentType'
    CONFIG_NOT_IN_WELL_KNOWN = 'ConfigNotInWellKnown'
    WELL_KNOWN_TOO_BIG = 'WellKnownTooBig'
    CONFIG_HTTP_NOT_FOUND = 'ConfigHttpNotFound'
    CONFIG_NO_RESPONSE = 'ConfigNoResponse'
    CONFIG_INVALID_RESPONSE = 'ConfigInvalidResponse'
    CONFIG_INVALID_CONTENT_TYPE = 'ConfigInvalidContentType'
    CLIENT_METADATA_HTTP_NOT_FOUND = 'ClientMetadataHttpNotFound'
    CLIENT_METADATA_NO_RESPONSE = 'ClientMetadataNoResponse'
    CLIENT_METADATA_INVALID_RESPONSE = 'ClientMetadataInvalidResponse'
    CLIENT_METADATA_INVALID_CONTENT_TYPE = 'ClientMetadataInvalidContentType'
    IDP_NOT_POTENTIALLY_TRUSTWORTHY = 'IdpNotPotentiallyTrustworthy'
    DISABLED_IN_SETTINGS = 'DisabledInSettings'
    DISABLED_IN_FLAGS = 'DisabledInFlags'
    ERROR_FETCHING_SIGNIN = 'ErrorFetchingSignin'
    INVALID_SIGNIN_RESPONSE = 'InvalidSigninResponse'
    ACCOUNTS_HTTP_NOT_FOUND = 'AccountsHttpNotFound'
    ACCOUNTS_NO_RESPONSE = 'AccountsNoResponse'
    ACCOUNTS_INVALID_RESPONSE = 'AccountsInvalidResponse'
    ACCOUNTS_LIST_EMPTY = 'AccountsListEmpty'
    ACCOUNTS_INVALID_CONTENT_TYPE = 'AccountsInvalidContentType'
    ID_TOKEN_HTTP_NOT_FOUND = 'IdTokenHttpNotFound'
    ID_TOKEN_NO_RESPONSE = 'IdTokenNoResponse'
    ID_TOKEN_INVALID_RESPONSE = 'IdTokenInvalidResponse'
    ID_TOKEN_IDP_ERROR_RESPONSE = 'IdTokenIdpErrorResponse'
    ID_TOKEN_CROSS_SITE_IDP_ERROR_RESPONSE = 'IdTokenCrossSiteIdpErrorResponse'
    ID_TOKEN_INVALID_REQUEST = 'IdTokenInvalidRequest'
    ID_TOKEN_INVALID_CONTENT_TYPE = 'IdTokenInvalidContentType'
    ERROR_ID_TOKEN = 'ErrorIdToken'
    CANCELED = 'Canceled'
    RP_PAGE_NOT_VISIBLE = 'RpPageNotVisible'
    SILENT_MEDIATION_FAILURE = 'SilentMediationFailure'
    THIRD_PARTY_COOKIES_BLOCKED = 'ThirdPartyCookiesBlocked'
    NOT_SIGNED_IN_WITH_IDP = 'NotSignedInWithIdp'
    MISSING_TRANSIENT_USER_ACTIVATION = 'MissingTransientUserActivation'
    REPLACED_BY_ACTIVE_MODE = 'ReplacedByActiveMode'
    INVALID_FIELDS_SPECIFIED = 'InvalidFieldsSpecified'
    RELYING_PARTY_ORIGIN_IS_OPAQUE = 'RelyingPartyOriginIsOpaque'
    TYPE_NOT_MATCHING = 'TypeNotMatching'
    UI_DISMISSED_NO_EMBARGO = 'UiDismissedNoEmbargo'
    CORS_ERROR = 'CorsError'
    SUPPRESSED_BY_SEGMENTATION_PLATFORM = 'SuppressedBySegmentationPlatform'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> FederatedAuthRequestIssueReason: ...

@dataclass
class FederatedAuthUserInfoRequestIssueDetails:
    federated_auth_user_info_request_issue_reason: FederatedAuthUserInfoRequestIssueReason
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FederatedAuthUserInfoRequestIssueDetails: ...

class FederatedAuthUserInfoRequestIssueReason(enum.Enum):
    NOT_SAME_ORIGIN = 'NotSameOrigin'
    NOT_IFRAME = 'NotIframe'
    NOT_POTENTIALLY_TRUSTWORTHY = 'NotPotentiallyTrustworthy'
    NO_API_PERMISSION = 'NoApiPermission'
    NOT_SIGNED_IN_WITH_IDP = 'NotSignedInWithIdp'
    NO_ACCOUNT_SHARING_PERMISSION = 'NoAccountSharingPermission'
    INVALID_CONFIG_OR_WELL_KNOWN = 'InvalidConfigOrWellKnown'
    INVALID_ACCOUNTS_RESPONSE = 'InvalidAccountsResponse'
    NO_RETURNING_USER_FROM_FETCHED_ACCOUNTS = 'NoReturningUserFromFetchedAccounts'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> FederatedAuthUserInfoRequestIssueReason: ...

@dataclass
class ClientHintIssueDetails:
    source_code_location: SourceCodeLocation
    client_hint_issue_reason: ClientHintIssueReason
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ClientHintIssueDetails: ...

@dataclass
class FailedRequestInfo:
    url: str
    failure_message: str
    request_id: network.RequestId | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FailedRequestInfo: ...

class PartitioningBlobURLInfo(enum.Enum):
    BLOCKED_CROSS_PARTITION_FETCHING = 'BlockedCrossPartitionFetching'
    ENFORCE_NOOPENER_FOR_NAVIGATION = 'EnforceNoopenerForNavigation'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PartitioningBlobURLInfo: ...

@dataclass
class PartitioningBlobURLIssueDetails:
    url: str
    partitioning_blob_url_info: PartitioningBlobURLInfo
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PartitioningBlobURLIssueDetails: ...

class ElementAccessibilityIssueReason(enum.Enum):
    DISALLOWED_SELECT_CHILD = 'DisallowedSelectChild'
    DISALLOWED_OPT_GROUP_CHILD = 'DisallowedOptGroupChild'
    NON_PHRASING_CONTENT_OPTION_CHILD = 'NonPhrasingContentOptionChild'
    INTERACTIVE_CONTENT_OPTION_CHILD = 'InteractiveContentOptionChild'
    INTERACTIVE_CONTENT_LEGEND_CHILD = 'InteractiveContentLegendChild'
    INTERACTIVE_CONTENT_SUMMARY_DESCENDANT = 'InteractiveContentSummaryDescendant'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ElementAccessibilityIssueReason: ...

@dataclass
class ElementAccessibilityIssueDetails:
    node_id: dom.BackendNodeId
    element_accessibility_issue_reason: ElementAccessibilityIssueReason
    has_disallowed_attributes: bool
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ElementAccessibilityIssueDetails: ...

class StyleSheetLoadingIssueReason(enum.Enum):
    LATE_IMPORT_RULE = 'LateImportRule'
    REQUEST_FAILED = 'RequestFailed'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> StyleSheetLoadingIssueReason: ...

@dataclass
class StylesheetLoadingIssueDetails:
    source_code_location: SourceCodeLocation
    style_sheet_loading_issue_reason: StyleSheetLoadingIssueReason
    failed_request_info: FailedRequestInfo | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> StylesheetLoadingIssueDetails: ...

class PropertyRuleIssueReason(enum.Enum):
    INVALID_SYNTAX = 'InvalidSyntax'
    INVALID_INITIAL_VALUE = 'InvalidInitialValue'
    INVALID_INHERITS = 'InvalidInherits'
    INVALID_NAME = 'InvalidName'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PropertyRuleIssueReason: ...

@dataclass
class PropertyRuleIssueDetails:
    source_code_location: SourceCodeLocation
    property_rule_issue_reason: PropertyRuleIssueReason
    property_value: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PropertyRuleIssueDetails: ...

class UserReidentificationIssueType(enum.Enum):
    BLOCKED_FRAME_NAVIGATION = 'BlockedFrameNavigation'
    BLOCKED_SUBRESOURCE = 'BlockedSubresource'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> UserReidentificationIssueType: ...

@dataclass
class UserReidentificationIssueDetails:
    type_: UserReidentificationIssueType
    request: AffectedRequest | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> UserReidentificationIssueDetails: ...

class InspectorIssueCode(enum.Enum):
    COOKIE_ISSUE = 'CookieIssue'
    MIXED_CONTENT_ISSUE = 'MixedContentIssue'
    BLOCKED_BY_RESPONSE_ISSUE = 'BlockedByResponseIssue'
    HEAVY_AD_ISSUE = 'HeavyAdIssue'
    CONTENT_SECURITY_POLICY_ISSUE = 'ContentSecurityPolicyIssue'
    SHARED_ARRAY_BUFFER_ISSUE = 'SharedArrayBufferIssue'
    LOW_TEXT_CONTRAST_ISSUE = 'LowTextContrastIssue'
    CORS_ISSUE = 'CorsIssue'
    ATTRIBUTION_REPORTING_ISSUE = 'AttributionReportingIssue'
    QUIRKS_MODE_ISSUE = 'QuirksModeIssue'
    PARTITIONING_BLOB_URL_ISSUE = 'PartitioningBlobURLIssue'
    NAVIGATOR_USER_AGENT_ISSUE = 'NavigatorUserAgentIssue'
    GENERIC_ISSUE = 'GenericIssue'
    DEPRECATION_ISSUE = 'DeprecationIssue'
    CLIENT_HINT_ISSUE = 'ClientHintIssue'
    FEDERATED_AUTH_REQUEST_ISSUE = 'FederatedAuthRequestIssue'
    BOUNCE_TRACKING_ISSUE = 'BounceTrackingIssue'
    COOKIE_DEPRECATION_METADATA_ISSUE = 'CookieDeprecationMetadataIssue'
    STYLESHEET_LOADING_ISSUE = 'StylesheetLoadingIssue'
    FEDERATED_AUTH_USER_INFO_REQUEST_ISSUE = 'FederatedAuthUserInfoRequestIssue'
    PROPERTY_RULE_ISSUE = 'PropertyRuleIssue'
    SHARED_DICTIONARY_ISSUE = 'SharedDictionaryIssue'
    ELEMENT_ACCESSIBILITY_ISSUE = 'ElementAccessibilityIssue'
    SRI_MESSAGE_SIGNATURE_ISSUE = 'SRIMessageSignatureIssue'
    USER_REIDENTIFICATION_ISSUE = 'UserReidentificationIssue'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> InspectorIssueCode: ...

@dataclass
class InspectorIssueDetails:
    cookie_issue_details: CookieIssueDetails | None = ...
    mixed_content_issue_details: MixedContentIssueDetails | None = ...
    blocked_by_response_issue_details: BlockedByResponseIssueDetails | None = ...
    heavy_ad_issue_details: HeavyAdIssueDetails | None = ...
    content_security_policy_issue_details: ContentSecurityPolicyIssueDetails | None = ...
    shared_array_buffer_issue_details: SharedArrayBufferIssueDetails | None = ...
    low_text_contrast_issue_details: LowTextContrastIssueDetails | None = ...
    cors_issue_details: CorsIssueDetails | None = ...
    attribution_reporting_issue_details: AttributionReportingIssueDetails | None = ...
    quirks_mode_issue_details: QuirksModeIssueDetails | None = ...
    partitioning_blob_url_issue_details: PartitioningBlobURLIssueDetails | None = ...
    navigator_user_agent_issue_details: NavigatorUserAgentIssueDetails | None = ...
    generic_issue_details: GenericIssueDetails | None = ...
    deprecation_issue_details: DeprecationIssueDetails | None = ...
    client_hint_issue_details: ClientHintIssueDetails | None = ...
    federated_auth_request_issue_details: FederatedAuthRequestIssueDetails | None = ...
    bounce_tracking_issue_details: BounceTrackingIssueDetails | None = ...
    cookie_deprecation_metadata_issue_details: CookieDeprecationMetadataIssueDetails | None = ...
    stylesheet_loading_issue_details: StylesheetLoadingIssueDetails | None = ...
    property_rule_issue_details: PropertyRuleIssueDetails | None = ...
    federated_auth_user_info_request_issue_details: FederatedAuthUserInfoRequestIssueDetails | None = ...
    shared_dictionary_issue_details: SharedDictionaryIssueDetails | None = ...
    element_accessibility_issue_details: ElementAccessibilityIssueDetails | None = ...
    sri_message_signature_issue_details: SRIMessageSignatureIssueDetails | None = ...
    user_reidentification_issue_details: UserReidentificationIssueDetails | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InspectorIssueDetails: ...

class IssueId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> IssueId: ...

@dataclass
class InspectorIssue:
    code: InspectorIssueCode
    details: InspectorIssueDetails
    issue_id: IssueId | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InspectorIssue: ...

def get_encoded_response(request_id: network.RequestId, encoding: str, quality: float | None = None, size_only: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[str | None, int, int]]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def check_contrast(report_aaa: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def check_forms_issues() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[GenericIssueDetails]]: ...

@dataclass
class IssueAdded:
    issue: InspectorIssue
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> IssueAdded: ...
