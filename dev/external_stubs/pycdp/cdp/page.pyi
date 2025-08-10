import enum
import typing
from . import debugger as debugger, dom as dom, emulation as emulation, io as io, network as network, runtime as runtime
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class FrameId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> FrameId: ...

class AdFrameType(enum.Enum):
    NONE = 'none'
    CHILD = 'child'
    ROOT = 'root'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AdFrameType: ...

class AdFrameExplanation(enum.Enum):
    PARENT_IS_AD = 'ParentIsAd'
    CREATED_BY_AD_SCRIPT = 'CreatedByAdScript'
    MATCHED_BLOCKING_RULE = 'MatchedBlockingRule'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AdFrameExplanation: ...

@dataclass
class AdFrameStatus:
    ad_frame_type: AdFrameType
    explanations: list[AdFrameExplanation] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AdFrameStatus: ...

@dataclass
class AdScriptId:
    script_id: runtime.ScriptId
    debugger_id: runtime.UniqueDebuggerId
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AdScriptId: ...

@dataclass
class AdScriptAncestry:
    ancestry_chain: list[AdScriptId]
    root_script_filterlist_rule: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AdScriptAncestry: ...

class SecureContextType(enum.Enum):
    SECURE = 'Secure'
    SECURE_LOCALHOST = 'SecureLocalhost'
    INSECURE_SCHEME = 'InsecureScheme'
    INSECURE_ANCESTOR = 'InsecureAncestor'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SecureContextType: ...

class CrossOriginIsolatedContextType(enum.Enum):
    ISOLATED = 'Isolated'
    NOT_ISOLATED = 'NotIsolated'
    NOT_ISOLATED_FEATURE_DISABLED = 'NotIsolatedFeatureDisabled'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CrossOriginIsolatedContextType: ...

class GatedAPIFeatures(enum.Enum):
    SHARED_ARRAY_BUFFERS = 'SharedArrayBuffers'
    SHARED_ARRAY_BUFFERS_TRANSFER_ALLOWED = 'SharedArrayBuffersTransferAllowed'
    PERFORMANCE_MEASURE_MEMORY = 'PerformanceMeasureMemory'
    PERFORMANCE_PROFILE = 'PerformanceProfile'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> GatedAPIFeatures: ...

class PermissionsPolicyFeature(enum.Enum):
    ACCELEROMETER = 'accelerometer'
    ALL_SCREENS_CAPTURE = 'all-screens-capture'
    AMBIENT_LIGHT_SENSOR = 'ambient-light-sensor'
    ARIA_NOTIFY = 'aria-notify'
    ATTRIBUTION_REPORTING = 'attribution-reporting'
    AUTOPLAY = 'autoplay'
    BLUETOOTH = 'bluetooth'
    BROWSING_TOPICS = 'browsing-topics'
    CAMERA = 'camera'
    CAPTURED_SURFACE_CONTROL = 'captured-surface-control'
    CH_DPR = 'ch-dpr'
    CH_DEVICE_MEMORY = 'ch-device-memory'
    CH_DOWNLINK = 'ch-downlink'
    CH_ECT = 'ch-ect'
    CH_PREFERS_COLOR_SCHEME = 'ch-prefers-color-scheme'
    CH_PREFERS_REDUCED_MOTION = 'ch-prefers-reduced-motion'
    CH_PREFERS_REDUCED_TRANSPARENCY = 'ch-prefers-reduced-transparency'
    CH_RTT = 'ch-rtt'
    CH_SAVE_DATA = 'ch-save-data'
    CH_UA = 'ch-ua'
    CH_UA_ARCH = 'ch-ua-arch'
    CH_UA_BITNESS = 'ch-ua-bitness'
    CH_UA_HIGH_ENTROPY_VALUES = 'ch-ua-high-entropy-values'
    CH_UA_PLATFORM = 'ch-ua-platform'
    CH_UA_MODEL = 'ch-ua-model'
    CH_UA_MOBILE = 'ch-ua-mobile'
    CH_UA_FORM_FACTORS = 'ch-ua-form-factors'
    CH_UA_FULL_VERSION = 'ch-ua-full-version'
    CH_UA_FULL_VERSION_LIST = 'ch-ua-full-version-list'
    CH_UA_PLATFORM_VERSION = 'ch-ua-platform-version'
    CH_UA_WOW64 = 'ch-ua-wow64'
    CH_VIEWPORT_HEIGHT = 'ch-viewport-height'
    CH_VIEWPORT_WIDTH = 'ch-viewport-width'
    CH_WIDTH = 'ch-width'
    CLIPBOARD_READ = 'clipboard-read'
    CLIPBOARD_WRITE = 'clipboard-write'
    COMPUTE_PRESSURE = 'compute-pressure'
    CONTROLLED_FRAME = 'controlled-frame'
    CROSS_ORIGIN_ISOLATED = 'cross-origin-isolated'
    DEFERRED_FETCH = 'deferred-fetch'
    DEFERRED_FETCH_MINIMAL = 'deferred-fetch-minimal'
    DEVICE_ATTRIBUTES = 'device-attributes'
    DIGITAL_CREDENTIALS_GET = 'digital-credentials-get'
    DIRECT_SOCKETS = 'direct-sockets'
    DIRECT_SOCKETS_PRIVATE = 'direct-sockets-private'
    DISPLAY_CAPTURE = 'display-capture'
    DOCUMENT_DOMAIN = 'document-domain'
    ENCRYPTED_MEDIA = 'encrypted-media'
    EXECUTION_WHILE_OUT_OF_VIEWPORT = 'execution-while-out-of-viewport'
    EXECUTION_WHILE_NOT_RENDERED = 'execution-while-not-rendered'
    FENCED_UNPARTITIONED_STORAGE_READ = 'fenced-unpartitioned-storage-read'
    FOCUS_WITHOUT_USER_ACTIVATION = 'focus-without-user-activation'
    FULLSCREEN = 'fullscreen'
    FROBULATE = 'frobulate'
    GAMEPAD = 'gamepad'
    GEOLOCATION = 'geolocation'
    GYROSCOPE = 'gyroscope'
    HID = 'hid'
    IDENTITY_CREDENTIALS_GET = 'identity-credentials-get'
    IDLE_DETECTION = 'idle-detection'
    INTEREST_COHORT = 'interest-cohort'
    JOIN_AD_INTEREST_GROUP = 'join-ad-interest-group'
    KEYBOARD_MAP = 'keyboard-map'
    LANGUAGE_DETECTOR = 'language-detector'
    LANGUAGE_MODEL = 'language-model'
    LOCAL_FONTS = 'local-fonts'
    LOCAL_NETWORK_ACCESS = 'local-network-access'
    MAGNETOMETER = 'magnetometer'
    MEDIA_PLAYBACK_WHILE_NOT_VISIBLE = 'media-playback-while-not-visible'
    MICROPHONE = 'microphone'
    MIDI = 'midi'
    ON_DEVICE_SPEECH_RECOGNITION = 'on-device-speech-recognition'
    OTP_CREDENTIALS = 'otp-credentials'
    PAYMENT = 'payment'
    PICTURE_IN_PICTURE = 'picture-in-picture'
    POPINS = 'popins'
    PRIVATE_AGGREGATION = 'private-aggregation'
    PRIVATE_STATE_TOKEN_ISSUANCE = 'private-state-token-issuance'
    PRIVATE_STATE_TOKEN_REDEMPTION = 'private-state-token-redemption'
    PUBLICKEY_CREDENTIALS_CREATE = 'publickey-credentials-create'
    PUBLICKEY_CREDENTIALS_GET = 'publickey-credentials-get'
    RECORD_AD_AUCTION_EVENTS = 'record-ad-auction-events'
    REWRITER = 'rewriter'
    RUN_AD_AUCTION = 'run-ad-auction'
    SCREEN_WAKE_LOCK = 'screen-wake-lock'
    SERIAL = 'serial'
    SHARED_AUTOFILL = 'shared-autofill'
    SHARED_STORAGE = 'shared-storage'
    SHARED_STORAGE_SELECT_URL = 'shared-storage-select-url'
    SMART_CARD = 'smart-card'
    SPEAKER_SELECTION = 'speaker-selection'
    STORAGE_ACCESS = 'storage-access'
    SUB_APPS = 'sub-apps'
    SUMMARIZER = 'summarizer'
    SYNC_XHR = 'sync-xhr'
    TRANSLATOR = 'translator'
    UNLOAD = 'unload'
    USB = 'usb'
    USB_UNRESTRICTED = 'usb-unrestricted'
    VERTICAL_SCROLL = 'vertical-scroll'
    WEB_APP_INSTALLATION = 'web-app-installation'
    WEB_PRINTING = 'web-printing'
    WEB_SHARE = 'web-share'
    WINDOW_MANAGEMENT = 'window-management'
    WRITER = 'writer'
    XR_SPATIAL_TRACKING = 'xr-spatial-tracking'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PermissionsPolicyFeature: ...

class PermissionsPolicyBlockReason(enum.Enum):
    HEADER = 'Header'
    IFRAME_ATTRIBUTE = 'IframeAttribute'
    IN_FENCED_FRAME_TREE = 'InFencedFrameTree'
    IN_ISOLATED_APP = 'InIsolatedApp'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PermissionsPolicyBlockReason: ...

@dataclass
class PermissionsPolicyBlockLocator:
    frame_id: FrameId
    block_reason: PermissionsPolicyBlockReason
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PermissionsPolicyBlockLocator: ...

@dataclass
class PermissionsPolicyFeatureState:
    feature: PermissionsPolicyFeature
    allowed: bool
    locator: PermissionsPolicyBlockLocator | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PermissionsPolicyFeatureState: ...

class OriginTrialTokenStatus(enum.Enum):
    SUCCESS = 'Success'
    NOT_SUPPORTED = 'NotSupported'
    INSECURE = 'Insecure'
    EXPIRED = 'Expired'
    WRONG_ORIGIN = 'WrongOrigin'
    INVALID_SIGNATURE = 'InvalidSignature'
    MALFORMED = 'Malformed'
    WRONG_VERSION = 'WrongVersion'
    FEATURE_DISABLED = 'FeatureDisabled'
    TOKEN_DISABLED = 'TokenDisabled'
    FEATURE_DISABLED_FOR_USER = 'FeatureDisabledForUser'
    UNKNOWN_TRIAL = 'UnknownTrial'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> OriginTrialTokenStatus: ...

class OriginTrialStatus(enum.Enum):
    ENABLED = 'Enabled'
    VALID_TOKEN_NOT_PROVIDED = 'ValidTokenNotProvided'
    OS_NOT_SUPPORTED = 'OSNotSupported'
    TRIAL_NOT_ALLOWED = 'TrialNotAllowed'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> OriginTrialStatus: ...

class OriginTrialUsageRestriction(enum.Enum):
    NONE = 'None'
    SUBSET = 'Subset'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> OriginTrialUsageRestriction: ...

@dataclass
class OriginTrialToken:
    origin: str
    match_sub_domains: bool
    trial_name: str
    expiry_time: network.TimeSinceEpoch
    is_third_party: bool
    usage_restriction: OriginTrialUsageRestriction
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> OriginTrialToken: ...

@dataclass
class OriginTrialTokenWithStatus:
    raw_token_text: str
    status: OriginTrialTokenStatus
    parsed_token: OriginTrialToken | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> OriginTrialTokenWithStatus: ...

@dataclass
class OriginTrial:
    trial_name: str
    status: OriginTrialStatus
    tokens_with_status: list[OriginTrialTokenWithStatus]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> OriginTrial: ...

@dataclass
class SecurityOriginDetails:
    is_localhost: bool
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SecurityOriginDetails: ...

@dataclass
class Frame:
    id_: FrameId
    loader_id: network.LoaderId
    url: str
    domain_and_registry: str
    security_origin: str
    mime_type: str
    secure_context_type: SecureContextType
    cross_origin_isolated_context_type: CrossOriginIsolatedContextType
    gated_api_features: list[GatedAPIFeatures]
    parent_id: FrameId | None = ...
    name: str | None = ...
    url_fragment: str | None = ...
    security_origin_details: SecurityOriginDetails | None = ...
    unreachable_url: str | None = ...
    ad_frame_status: AdFrameStatus | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Frame: ...

@dataclass
class FrameResource:
    url: str
    type_: network.ResourceType
    mime_type: str
    last_modified: network.TimeSinceEpoch | None = ...
    content_size: float | None = ...
    failed: bool | None = ...
    canceled: bool | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameResource: ...

@dataclass
class FrameResourceTree:
    frame: Frame
    resources: list[FrameResource]
    child_frames: list[FrameResourceTree] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameResourceTree: ...

@dataclass
class FrameTree:
    frame: Frame
    child_frames: list[FrameTree] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameTree: ...

class ScriptIdentifier(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ScriptIdentifier: ...

class TransitionType(enum.Enum):
    LINK = 'link'
    TYPED = 'typed'
    ADDRESS_BAR = 'address_bar'
    AUTO_BOOKMARK = 'auto_bookmark'
    AUTO_SUBFRAME = 'auto_subframe'
    MANUAL_SUBFRAME = 'manual_subframe'
    GENERATED = 'generated'
    AUTO_TOPLEVEL = 'auto_toplevel'
    FORM_SUBMIT = 'form_submit'
    RELOAD = 'reload'
    KEYWORD = 'keyword'
    KEYWORD_GENERATED = 'keyword_generated'
    OTHER = 'other'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> TransitionType: ...

@dataclass
class NavigationEntry:
    id_: int
    url: str
    user_typed_url: str
    title: str
    transition_type: TransitionType
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> NavigationEntry: ...

@dataclass
class ScreencastFrameMetadata:
    offset_top: float
    page_scale_factor: float
    device_width: float
    device_height: float
    scroll_offset_x: float
    scroll_offset_y: float
    timestamp: network.TimeSinceEpoch | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScreencastFrameMetadata: ...

class DialogType(enum.Enum):
    ALERT = 'alert'
    CONFIRM = 'confirm'
    PROMPT = 'prompt'
    BEFOREUNLOAD = 'beforeunload'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> DialogType: ...

@dataclass
class AppManifestError:
    message: str
    critical: int
    line: int
    column: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AppManifestError: ...

@dataclass
class AppManifestParsedProperties:
    scope: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AppManifestParsedProperties: ...

@dataclass
class LayoutViewport:
    page_x: int
    page_y: int
    client_width: int
    client_height: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LayoutViewport: ...

@dataclass
class VisualViewport:
    offset_x: float
    offset_y: float
    page_x: float
    page_y: float
    client_width: float
    client_height: float
    scale: float
    zoom: float | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> VisualViewport: ...

@dataclass
class Viewport:
    x: float
    y: float
    width: float
    height: float
    scale: float
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Viewport: ...

@dataclass
class FontFamilies:
    standard: str | None = ...
    fixed: str | None = ...
    serif: str | None = ...
    sans_serif: str | None = ...
    cursive: str | None = ...
    fantasy: str | None = ...
    math: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FontFamilies: ...

@dataclass
class ScriptFontFamilies:
    script: str
    font_families: FontFamilies
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScriptFontFamilies: ...

@dataclass
class FontSizes:
    standard: int | None = ...
    fixed: int | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FontSizes: ...

class ClientNavigationReason(enum.Enum):
    ANCHOR_CLICK = 'anchorClick'
    FORM_SUBMISSION_GET = 'formSubmissionGet'
    FORM_SUBMISSION_POST = 'formSubmissionPost'
    HTTP_HEADER_REFRESH = 'httpHeaderRefresh'
    INITIAL_FRAME_NAVIGATION = 'initialFrameNavigation'
    META_TAG_REFRESH = 'metaTagRefresh'
    OTHER = 'other'
    PAGE_BLOCK_INTERSTITIAL = 'pageBlockInterstitial'
    RELOAD = 'reload'
    SCRIPT_INITIATED = 'scriptInitiated'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ClientNavigationReason: ...

class ClientNavigationDisposition(enum.Enum):
    CURRENT_TAB = 'currentTab'
    NEW_TAB = 'newTab'
    NEW_WINDOW = 'newWindow'
    DOWNLOAD = 'download'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ClientNavigationDisposition: ...

@dataclass
class InstallabilityErrorArgument:
    name: str
    value: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InstallabilityErrorArgument: ...

@dataclass
class InstallabilityError:
    error_id: str
    error_arguments: list[InstallabilityErrorArgument]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InstallabilityError: ...

class ReferrerPolicy(enum.Enum):
    NO_REFERRER = 'noReferrer'
    NO_REFERRER_WHEN_DOWNGRADE = 'noReferrerWhenDowngrade'
    ORIGIN = 'origin'
    ORIGIN_WHEN_CROSS_ORIGIN = 'originWhenCrossOrigin'
    SAME_ORIGIN = 'sameOrigin'
    STRICT_ORIGIN = 'strictOrigin'
    STRICT_ORIGIN_WHEN_CROSS_ORIGIN = 'strictOriginWhenCrossOrigin'
    UNSAFE_URL = 'unsafeUrl'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ReferrerPolicy: ...

@dataclass
class CompilationCacheParams:
    url: str
    eager: bool | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CompilationCacheParams: ...

@dataclass
class FileFilter:
    name: str | None = ...
    accepts: list[str] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FileFilter: ...

@dataclass
class FileHandler:
    action: str
    name: str
    launch_type: str
    icons: list[ImageResource] | None = ...
    accepts: list[FileFilter] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FileHandler: ...

@dataclass
class ImageResource:
    url: str
    sizes: str | None = ...
    type_: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ImageResource: ...

@dataclass
class LaunchHandler:
    client_mode: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LaunchHandler: ...

@dataclass
class ProtocolHandler:
    protocol: str
    url: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ProtocolHandler: ...

@dataclass
class RelatedApplication:
    url: str
    id_: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RelatedApplication: ...

@dataclass
class ScopeExtension:
    origin: str
    has_origin_wildcard: bool
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScopeExtension: ...

@dataclass
class Screenshot:
    image: ImageResource
    form_factor: str
    label: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Screenshot: ...

@dataclass
class ShareTarget:
    action: str
    method: str
    enctype: str
    title: str | None = ...
    text: str | None = ...
    url: str | None = ...
    files: list[FileFilter] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ShareTarget: ...

@dataclass
class Shortcut:
    name: str
    url: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Shortcut: ...

@dataclass
class WebAppManifest:
    background_color: str | None = ...
    description: str | None = ...
    dir_: str | None = ...
    display: str | None = ...
    display_overrides: list[str] | None = ...
    file_handlers: list[FileHandler] | None = ...
    icons: list[ImageResource] | None = ...
    id_: str | None = ...
    lang: str | None = ...
    launch_handler: LaunchHandler | None = ...
    name: str | None = ...
    orientation: str | None = ...
    prefer_related_applications: bool | None = ...
    protocol_handlers: list[ProtocolHandler] | None = ...
    related_applications: list[RelatedApplication] | None = ...
    scope: str | None = ...
    scope_extensions: list[ScopeExtension] | None = ...
    screenshots: list[Screenshot] | None = ...
    share_target: ShareTarget | None = ...
    short_name: str | None = ...
    shortcuts: list[Shortcut] | None = ...
    start_url: str | None = ...
    theme_color: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WebAppManifest: ...

class NavigationType(enum.Enum):
    NAVIGATION = 'Navigation'
    BACK_FORWARD_CACHE_RESTORE = 'BackForwardCacheRestore'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> NavigationType: ...

class BackForwardCacheNotRestoredReason(enum.Enum):
    NOT_PRIMARY_MAIN_FRAME = 'NotPrimaryMainFrame'
    BACK_FORWARD_CACHE_DISABLED = 'BackForwardCacheDisabled'
    RELATED_ACTIVE_CONTENTS_EXIST = 'RelatedActiveContentsExist'
    HTTP_STATUS_NOT_OK = 'HTTPStatusNotOK'
    SCHEME_NOT_HTTP_OR_HTTPS = 'SchemeNotHTTPOrHTTPS'
    LOADING = 'Loading'
    WAS_GRANTED_MEDIA_ACCESS = 'WasGrantedMediaAccess'
    DISABLE_FOR_RENDER_FRAME_HOST_CALLED = 'DisableForRenderFrameHostCalled'
    DOMAIN_NOT_ALLOWED = 'DomainNotAllowed'
    HTTP_METHOD_NOT_GET = 'HTTPMethodNotGET'
    SUBFRAME_IS_NAVIGATING = 'SubframeIsNavigating'
    TIMEOUT = 'Timeout'
    CACHE_LIMIT = 'CacheLimit'
    JAVA_SCRIPT_EXECUTION = 'JavaScriptExecution'
    RENDERER_PROCESS_KILLED = 'RendererProcessKilled'
    RENDERER_PROCESS_CRASHED = 'RendererProcessCrashed'
    SCHEDULER_TRACKED_FEATURE_USED = 'SchedulerTrackedFeatureUsed'
    CONFLICTING_BROWSING_INSTANCE = 'ConflictingBrowsingInstance'
    CACHE_FLUSHED = 'CacheFlushed'
    SERVICE_WORKER_VERSION_ACTIVATION = 'ServiceWorkerVersionActivation'
    SESSION_RESTORED = 'SessionRestored'
    SERVICE_WORKER_POST_MESSAGE = 'ServiceWorkerPostMessage'
    ENTERED_BACK_FORWARD_CACHE_BEFORE_SERVICE_WORKER_HOST_ADDED = 'EnteredBackForwardCacheBeforeServiceWorkerHostAdded'
    RENDER_FRAME_HOST_REUSED_SAME_SITE = 'RenderFrameHostReused_SameSite'
    RENDER_FRAME_HOST_REUSED_CROSS_SITE = 'RenderFrameHostReused_CrossSite'
    SERVICE_WORKER_CLAIM = 'ServiceWorkerClaim'
    IGNORE_EVENT_AND_EVICT = 'IgnoreEventAndEvict'
    HAVE_INNER_CONTENTS = 'HaveInnerContents'
    TIMEOUT_PUTTING_IN_CACHE = 'TimeoutPuttingInCache'
    BACK_FORWARD_CACHE_DISABLED_BY_LOW_MEMORY = 'BackForwardCacheDisabledByLowMemory'
    BACK_FORWARD_CACHE_DISABLED_BY_COMMAND_LINE = 'BackForwardCacheDisabledByCommandLine'
    NETWORK_REQUEST_DATAPIPE_DRAINED_AS_BYTES_CONSUMER = 'NetworkRequestDatapipeDrainedAsBytesConsumer'
    NETWORK_REQUEST_REDIRECTED = 'NetworkRequestRedirected'
    NETWORK_REQUEST_TIMEOUT = 'NetworkRequestTimeout'
    NETWORK_EXCEEDS_BUFFER_LIMIT = 'NetworkExceedsBufferLimit'
    NAVIGATION_CANCELLED_WHILE_RESTORING = 'NavigationCancelledWhileRestoring'
    NOT_MOST_RECENT_NAVIGATION_ENTRY = 'NotMostRecentNavigationEntry'
    BACK_FORWARD_CACHE_DISABLED_FOR_PRERENDER = 'BackForwardCacheDisabledForPrerender'
    USER_AGENT_OVERRIDE_DIFFERS = 'UserAgentOverrideDiffers'
    FOREGROUND_CACHE_LIMIT = 'ForegroundCacheLimit'
    BROWSING_INSTANCE_NOT_SWAPPED = 'BrowsingInstanceNotSwapped'
    BACK_FORWARD_CACHE_DISABLED_FOR_DELEGATE = 'BackForwardCacheDisabledForDelegate'
    UNLOAD_HANDLER_EXISTS_IN_MAIN_FRAME = 'UnloadHandlerExistsInMainFrame'
    UNLOAD_HANDLER_EXISTS_IN_SUB_FRAME = 'UnloadHandlerExistsInSubFrame'
    SERVICE_WORKER_UNREGISTRATION = 'ServiceWorkerUnregistration'
    CACHE_CONTROL_NO_STORE = 'CacheControlNoStore'
    CACHE_CONTROL_NO_STORE_COOKIE_MODIFIED = 'CacheControlNoStoreCookieModified'
    CACHE_CONTROL_NO_STORE_HTTP_ONLY_COOKIE_MODIFIED = 'CacheControlNoStoreHTTPOnlyCookieModified'
    NO_RESPONSE_HEAD = 'NoResponseHead'
    UNKNOWN = 'Unknown'
    ACTIVATION_NAVIGATIONS_DISALLOWED_FOR_BUG1234857 = 'ActivationNavigationsDisallowedForBug1234857'
    ERROR_DOCUMENT = 'ErrorDocument'
    FENCED_FRAMES_EMBEDDER = 'FencedFramesEmbedder'
    COOKIE_DISABLED = 'CookieDisabled'
    HTTP_AUTH_REQUIRED = 'HTTPAuthRequired'
    COOKIE_FLUSHED = 'CookieFlushed'
    BROADCAST_CHANNEL_ON_MESSAGE = 'BroadcastChannelOnMessage'
    WEB_VIEW_SETTINGS_CHANGED = 'WebViewSettingsChanged'
    WEB_VIEW_JAVA_SCRIPT_OBJECT_CHANGED = 'WebViewJavaScriptObjectChanged'
    WEB_VIEW_MESSAGE_LISTENER_INJECTED = 'WebViewMessageListenerInjected'
    WEB_VIEW_SAFE_BROWSING_ALLOWLIST_CHANGED = 'WebViewSafeBrowsingAllowlistChanged'
    WEB_VIEW_DOCUMENT_START_JAVASCRIPT_CHANGED = 'WebViewDocumentStartJavascriptChanged'
    WEB_SOCKET = 'WebSocket'
    WEB_TRANSPORT = 'WebTransport'
    WEB_RTC = 'WebRTC'
    MAIN_RESOURCE_HAS_CACHE_CONTROL_NO_STORE = 'MainResourceHasCacheControlNoStore'
    MAIN_RESOURCE_HAS_CACHE_CONTROL_NO_CACHE = 'MainResourceHasCacheControlNoCache'
    SUBRESOURCE_HAS_CACHE_CONTROL_NO_STORE = 'SubresourceHasCacheControlNoStore'
    SUBRESOURCE_HAS_CACHE_CONTROL_NO_CACHE = 'SubresourceHasCacheControlNoCache'
    CONTAINS_PLUGINS = 'ContainsPlugins'
    DOCUMENT_LOADED = 'DocumentLoaded'
    OUTSTANDING_NETWORK_REQUEST_OTHERS = 'OutstandingNetworkRequestOthers'
    REQUESTED_MIDI_PERMISSION = 'RequestedMIDIPermission'
    REQUESTED_AUDIO_CAPTURE_PERMISSION = 'RequestedAudioCapturePermission'
    REQUESTED_VIDEO_CAPTURE_PERMISSION = 'RequestedVideoCapturePermission'
    REQUESTED_BACK_FORWARD_CACHE_BLOCKED_SENSORS = 'RequestedBackForwardCacheBlockedSensors'
    REQUESTED_BACKGROUND_WORK_PERMISSION = 'RequestedBackgroundWorkPermission'
    BROADCAST_CHANNEL = 'BroadcastChannel'
    WEB_XR = 'WebXR'
    SHARED_WORKER = 'SharedWorker'
    SHARED_WORKER_MESSAGE = 'SharedWorkerMessage'
    WEB_LOCKS = 'WebLocks'
    WEB_HID = 'WebHID'
    WEB_SHARE = 'WebShare'
    REQUESTED_STORAGE_ACCESS_GRANT = 'RequestedStorageAccessGrant'
    WEB_NFC = 'WebNfc'
    OUTSTANDING_NETWORK_REQUEST_FETCH = 'OutstandingNetworkRequestFetch'
    OUTSTANDING_NETWORK_REQUEST_XHR = 'OutstandingNetworkRequestXHR'
    APP_BANNER = 'AppBanner'
    PRINTING = 'Printing'
    WEB_DATABASE = 'WebDatabase'
    PICTURE_IN_PICTURE = 'PictureInPicture'
    SPEECH_RECOGNIZER = 'SpeechRecognizer'
    IDLE_MANAGER = 'IdleManager'
    PAYMENT_MANAGER = 'PaymentManager'
    SPEECH_SYNTHESIS = 'SpeechSynthesis'
    KEYBOARD_LOCK = 'KeyboardLock'
    WEB_OTP_SERVICE = 'WebOTPService'
    OUTSTANDING_NETWORK_REQUEST_DIRECT_SOCKET = 'OutstandingNetworkRequestDirectSocket'
    INJECTED_JAVASCRIPT = 'InjectedJavascript'
    INJECTED_STYLE_SHEET = 'InjectedStyleSheet'
    KEEPALIVE_REQUEST = 'KeepaliveRequest'
    INDEXED_DB_EVENT = 'IndexedDBEvent'
    DUMMY = 'Dummy'
    JS_NETWORK_REQUEST_RECEIVED_CACHE_CONTROL_NO_STORE_RESOURCE = 'JsNetworkRequestReceivedCacheControlNoStoreResource'
    WEB_RTC_STICKY = 'WebRTCSticky'
    WEB_TRANSPORT_STICKY = 'WebTransportSticky'
    WEB_SOCKET_STICKY = 'WebSocketSticky'
    SMART_CARD = 'SmartCard'
    LIVE_MEDIA_STREAM_TRACK = 'LiveMediaStreamTrack'
    UNLOAD_HANDLER = 'UnloadHandler'
    PARSER_ABORTED = 'ParserAborted'
    CONTENT_SECURITY_HANDLER = 'ContentSecurityHandler'
    CONTENT_WEB_AUTHENTICATION_API = 'ContentWebAuthenticationAPI'
    CONTENT_FILE_CHOOSER = 'ContentFileChooser'
    CONTENT_SERIAL = 'ContentSerial'
    CONTENT_FILE_SYSTEM_ACCESS = 'ContentFileSystemAccess'
    CONTENT_MEDIA_DEVICES_DISPATCHER_HOST = 'ContentMediaDevicesDispatcherHost'
    CONTENT_WEB_BLUETOOTH = 'ContentWebBluetooth'
    CONTENT_WEB_USB = 'ContentWebUSB'
    CONTENT_MEDIA_SESSION_SERVICE = 'ContentMediaSessionService'
    CONTENT_SCREEN_READER = 'ContentScreenReader'
    CONTENT_DISCARDED = 'ContentDiscarded'
    EMBEDDER_POPUP_BLOCKER_TAB_HELPER = 'EmbedderPopupBlockerTabHelper'
    EMBEDDER_SAFE_BROWSING_TRIGGERED_POPUP_BLOCKER = 'EmbedderSafeBrowsingTriggeredPopupBlocker'
    EMBEDDER_SAFE_BROWSING_THREAT_DETAILS = 'EmbedderSafeBrowsingThreatDetails'
    EMBEDDER_APP_BANNER_MANAGER = 'EmbedderAppBannerManager'
    EMBEDDER_DOM_DISTILLER_VIEWER_SOURCE = 'EmbedderDomDistillerViewerSource'
    EMBEDDER_DOM_DISTILLER_SELF_DELETING_REQUEST_DELEGATE = 'EmbedderDomDistillerSelfDeletingRequestDelegate'
    EMBEDDER_OOM_INTERVENTION_TAB_HELPER = 'EmbedderOomInterventionTabHelper'
    EMBEDDER_OFFLINE_PAGE = 'EmbedderOfflinePage'
    EMBEDDER_CHROME_PASSWORD_MANAGER_CLIENT_BIND_CREDENTIAL_MANAGER = 'EmbedderChromePasswordManagerClientBindCredentialManager'
    EMBEDDER_PERMISSION_REQUEST_MANAGER = 'EmbedderPermissionRequestManager'
    EMBEDDER_MODAL_DIALOG = 'EmbedderModalDialog'
    EMBEDDER_EXTENSIONS = 'EmbedderExtensions'
    EMBEDDER_EXTENSION_MESSAGING = 'EmbedderExtensionMessaging'
    EMBEDDER_EXTENSION_MESSAGING_FOR_OPEN_PORT = 'EmbedderExtensionMessagingForOpenPort'
    EMBEDDER_EXTENSION_SENT_MESSAGE_TO_CACHED_FRAME = 'EmbedderExtensionSentMessageToCachedFrame'
    REQUESTED_BY_WEB_VIEW_CLIENT = 'RequestedByWebViewClient'
    POST_MESSAGE_BY_WEB_VIEW_CLIENT = 'PostMessageByWebViewClient'
    CACHE_CONTROL_NO_STORE_DEVICE_BOUND_SESSION_TERMINATED = 'CacheControlNoStoreDeviceBoundSessionTerminated'
    CACHE_LIMIT_PRUNED_ON_MODERATE_MEMORY_PRESSURE = 'CacheLimitPrunedOnModerateMemoryPressure'
    CACHE_LIMIT_PRUNED_ON_CRITICAL_MEMORY_PRESSURE = 'CacheLimitPrunedOnCriticalMemoryPressure'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> BackForwardCacheNotRestoredReason: ...

class BackForwardCacheNotRestoredReasonType(enum.Enum):
    SUPPORT_PENDING = 'SupportPending'
    PAGE_SUPPORT_NEEDED = 'PageSupportNeeded'
    CIRCUMSTANTIAL = 'Circumstantial'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> BackForwardCacheNotRestoredReasonType: ...

@dataclass
class BackForwardCacheBlockingDetails:
    line_number: int
    column_number: int
    url: str | None = ...
    function: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackForwardCacheBlockingDetails: ...

@dataclass
class BackForwardCacheNotRestoredExplanation:
    type_: BackForwardCacheNotRestoredReasonType
    reason: BackForwardCacheNotRestoredReason
    context: str | None = ...
    details: list[BackForwardCacheBlockingDetails] | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackForwardCacheNotRestoredExplanation: ...

@dataclass
class BackForwardCacheNotRestoredExplanationTree:
    url: str
    explanations: list[BackForwardCacheNotRestoredExplanation]
    children: list[BackForwardCacheNotRestoredExplanationTree]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackForwardCacheNotRestoredExplanationTree: ...

def add_script_to_evaluate_on_load(script_source: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, ScriptIdentifier]: ...
def add_script_to_evaluate_on_new_document(source: str, world_name: str | None = None, include_command_line_api: bool | None = None, run_immediately: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, ScriptIdentifier]: ...
def bring_to_front() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def capture_screenshot(format_: str | None = None, quality: int | None = None, clip: Viewport | None = None, from_surface: bool | None = None, capture_beyond_viewport: bool | None = None, optimize_for_speed: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, str]: ...
def capture_snapshot(format_: str | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, str]: ...
def clear_device_metrics_override() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_device_orientation_override() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_geolocation_override() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def create_isolated_world(frame_id: FrameId, world_name: str | None = None, grant_univeral_access: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, runtime.ExecutionContextId]: ...
def delete_cookie(cookie_name: str, url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable(enable_file_chooser_opened_event: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_app_manifest(manifest_id: str | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[str, list[AppManifestError], str | None, AppManifestParsedProperties | None, WebAppManifest]]: ...
def get_installability_errors() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[InstallabilityError]]: ...
def get_manifest_icons() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, str | None]: ...
def get_app_id() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[str | None, str | None]]: ...
def get_ad_script_ancestry(frame_id: FrameId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, AdScriptAncestry | None]: ...
def get_frame_tree() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, FrameTree]: ...
def get_layout_metrics() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[LayoutViewport, VisualViewport, dom.Rect, LayoutViewport, VisualViewport, dom.Rect]]: ...
def get_navigation_history() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[int, list[NavigationEntry]]]: ...
def reset_navigation_history() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_resource_content(frame_id: FrameId, url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[str, bool]]: ...
def get_resource_tree() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, FrameResourceTree]: ...
def handle_java_script_dialog(accept: bool, prompt_text: str | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def navigate(url: str, referrer: str | None = None, transition_type: TransitionType | None = None, frame_id: FrameId | None = None, referrer_policy: ReferrerPolicy | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[FrameId, network.LoaderId | None, str | None, bool | None]]: ...
def navigate_to_history_entry(entry_id: int) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def print_to_pdf(landscape: bool | None = None, display_header_footer: bool | None = None, print_background: bool | None = None, scale: float | None = None, paper_width: float | None = None, paper_height: float | None = None, margin_top: float | None = None, margin_bottom: float | None = None, margin_left: float | None = None, margin_right: float | None = None, page_ranges: str | None = None, header_template: str | None = None, footer_template: str | None = None, prefer_css_page_size: bool | None = None, transfer_mode: str | None = None, generate_tagged_pdf: bool | None = None, generate_document_outline: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[str, io.StreamHandle | None]]: ...
def reload(ignore_cache: bool | None = None, script_to_evaluate_on_load: str | None = None, loader_id: network.LoaderId | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def remove_script_to_evaluate_on_load(identifier: ScriptIdentifier) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def remove_script_to_evaluate_on_new_document(identifier: ScriptIdentifier) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def screencast_frame_ack(session_id: int) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def search_in_resource(frame_id: FrameId, url: str, query: str, case_sensitive: bool | None = None, is_regex: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[debugger.SearchMatch]]: ...
def set_ad_blocking_enabled(enabled: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_bypass_csp(enabled: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_permissions_policy_state(frame_id: FrameId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[PermissionsPolicyFeatureState]]: ...
def get_origin_trials(frame_id: FrameId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[OriginTrial]]: ...
def set_device_metrics_override(width: int, height: int, device_scale_factor: float, mobile: bool, scale: float | None = None, screen_width: int | None = None, screen_height: int | None = None, position_x: int | None = None, position_y: int | None = None, dont_set_visible_size: bool | None = None, screen_orientation: emulation.ScreenOrientation | None = None, viewport: Viewport | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_device_orientation_override(alpha: float, beta: float, gamma: float) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_font_families(font_families: FontFamilies, for_scripts: list[ScriptFontFamilies] | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_font_sizes(font_sizes: FontSizes) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_document_content(frame_id: FrameId, html: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_download_behavior(behavior: str, download_path: str | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_geolocation_override(latitude: float | None = None, longitude: float | None = None, accuracy: float | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_lifecycle_events_enabled(enabled: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_touch_emulation_enabled(enabled: bool, configuration: str | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def start_screencast(format_: str | None = None, quality: int | None = None, max_width: int | None = None, max_height: int | None = None, every_nth_frame: int | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def stop_loading() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def crash() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def close() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_web_lifecycle_state(state: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def stop_screencast() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def produce_compilation_cache(scripts: list[CompilationCacheParams]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def add_compilation_cache(url: str, data: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_compilation_cache() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_spc_transaction_mode(mode: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_rph_registration_mode(mode: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def generate_test_report(message: str, group: str | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def wait_for_debugger() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_intercept_file_chooser_dialog(enabled: bool, cancel: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_prerendering_allowed(is_allowed: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class DomContentEventFired:
    timestamp: network.MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DomContentEventFired: ...

@dataclass
class FileChooserOpened:
    frame_id: FrameId
    mode: str
    backend_node_id: dom.BackendNodeId | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FileChooserOpened: ...

@dataclass
class FrameAttached:
    frame_id: FrameId
    parent_frame_id: FrameId
    stack: runtime.StackTrace | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameAttached: ...

@dataclass
class FrameClearedScheduledNavigation:
    frame_id: FrameId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameClearedScheduledNavigation: ...

@dataclass
class FrameDetached:
    frame_id: FrameId
    reason: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameDetached: ...

@dataclass
class FrameSubtreeWillBeDetached:
    frame_id: FrameId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameSubtreeWillBeDetached: ...

@dataclass
class FrameNavigated:
    frame: Frame
    type_: NavigationType
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameNavigated: ...

@dataclass
class DocumentOpened:
    frame: Frame
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DocumentOpened: ...

@dataclass
class FrameResized:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameResized: ...

@dataclass
class FrameStartedNavigating:
    frame_id: FrameId
    url: str
    loader_id: network.LoaderId
    navigation_type: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameStartedNavigating: ...

@dataclass
class FrameRequestedNavigation:
    frame_id: FrameId
    reason: ClientNavigationReason
    url: str
    disposition: ClientNavigationDisposition
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameRequestedNavigation: ...

@dataclass
class FrameScheduledNavigation:
    frame_id: FrameId
    delay: float
    reason: ClientNavigationReason
    url: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameScheduledNavigation: ...

@dataclass
class FrameStartedLoading:
    frame_id: FrameId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameStartedLoading: ...

@dataclass
class FrameStoppedLoading:
    frame_id: FrameId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameStoppedLoading: ...

@dataclass
class DownloadWillBegin:
    frame_id: FrameId
    guid: str
    url: str
    suggested_filename: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DownloadWillBegin: ...

@dataclass
class DownloadProgress:
    guid: str
    total_bytes: float
    received_bytes: float
    state: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DownloadProgress: ...

@dataclass
class InterstitialHidden:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InterstitialHidden: ...

@dataclass
class InterstitialShown:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InterstitialShown: ...

@dataclass
class JavascriptDialogClosed:
    frame_id: FrameId
    result: bool
    user_input: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> JavascriptDialogClosed: ...

@dataclass
class JavascriptDialogOpening:
    url: str
    frame_id: FrameId
    message: str
    type_: DialogType
    has_browser_handler: bool
    default_prompt: str | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> JavascriptDialogOpening: ...

@dataclass
class LifecycleEvent:
    frame_id: FrameId
    loader_id: network.LoaderId
    name: str
    timestamp: network.MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LifecycleEvent: ...

@dataclass
class BackForwardCacheNotUsed:
    loader_id: network.LoaderId
    frame_id: FrameId
    not_restored_explanations: list[BackForwardCacheNotRestoredExplanation]
    not_restored_explanations_tree: BackForwardCacheNotRestoredExplanationTree | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackForwardCacheNotUsed: ...

@dataclass
class LoadEventFired:
    timestamp: network.MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LoadEventFired: ...

@dataclass
class NavigatedWithinDocument:
    frame_id: FrameId
    url: str
    navigation_type: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> NavigatedWithinDocument: ...

@dataclass
class ScreencastFrame:
    data: str
    metadata: ScreencastFrameMetadata
    session_id: int
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScreencastFrame: ...

@dataclass
class ScreencastVisibilityChanged:
    visible: bool
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScreencastVisibilityChanged: ...

@dataclass
class WindowOpen:
    url: str
    window_name: str
    window_features: list[str]
    user_gesture: bool
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WindowOpen: ...

@dataclass
class CompilationCacheProduced:
    url: str
    data: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CompilationCacheProduced: ...
