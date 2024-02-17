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
    NONE: str
    CHILD: str
    ROOT: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AdFrameType: ...

class AdFrameExplanation(enum.Enum):
    PARENT_IS_AD: str
    CREATED_BY_AD_SCRIPT: str
    MATCHED_BLOCKING_RULE: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AdFrameExplanation: ...

@dataclass
class AdFrameStatus:
    ad_frame_type: AdFrameType
    explanations: typing.Optional[typing.List[AdFrameExplanation]] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AdFrameStatus: ...
    def __init__(self, ad_frame_type, explanations) -> None: ...

@dataclass
class AdScriptId:
    script_id: runtime.ScriptId
    debugger_id: runtime.UniqueDebuggerId
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AdScriptId: ...
    def __init__(self, script_id, debugger_id) -> None: ...

class SecureContextType(enum.Enum):
    SECURE: str
    SECURE_LOCALHOST: str
    INSECURE_SCHEME: str
    INSECURE_ANCESTOR: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SecureContextType: ...

class CrossOriginIsolatedContextType(enum.Enum):
    ISOLATED: str
    NOT_ISOLATED: str
    NOT_ISOLATED_FEATURE_DISABLED: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CrossOriginIsolatedContextType: ...

class GatedAPIFeatures(enum.Enum):
    SHARED_ARRAY_BUFFERS: str
    SHARED_ARRAY_BUFFERS_TRANSFER_ALLOWED: str
    PERFORMANCE_MEASURE_MEMORY: str
    PERFORMANCE_PROFILE: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> GatedAPIFeatures: ...

class PermissionsPolicyFeature(enum.Enum):
    ACCELEROMETER: str
    AMBIENT_LIGHT_SENSOR: str
    ATTRIBUTION_REPORTING: str
    AUTOPLAY: str
    BLUETOOTH: str
    BROWSING_TOPICS: str
    CAMERA: str
    CAPTURED_SURFACE_CONTROL: str
    CH_DPR: str
    CH_DEVICE_MEMORY: str
    CH_DOWNLINK: str
    CH_ECT: str
    CH_PREFERS_COLOR_SCHEME: str
    CH_PREFERS_REDUCED_MOTION: str
    CH_PREFERS_REDUCED_TRANSPARENCY: str
    CH_RTT: str
    CH_SAVE_DATA: str
    CH_UA: str
    CH_UA_ARCH: str
    CH_UA_BITNESS: str
    CH_UA_PLATFORM: str
    CH_UA_MODEL: str
    CH_UA_MOBILE: str
    CH_UA_FORM_FACTOR: str
    CH_UA_FULL_VERSION: str
    CH_UA_FULL_VERSION_LIST: str
    CH_UA_PLATFORM_VERSION: str
    CH_UA_WOW64: str
    CH_VIEWPORT_HEIGHT: str
    CH_VIEWPORT_WIDTH: str
    CH_WIDTH: str
    CLIPBOARD_READ: str
    CLIPBOARD_WRITE: str
    COMPUTE_PRESSURE: str
    CROSS_ORIGIN_ISOLATED: str
    DIRECT_SOCKETS: str
    DISPLAY_CAPTURE: str
    DOCUMENT_DOMAIN: str
    ENCRYPTED_MEDIA: str
    EXECUTION_WHILE_OUT_OF_VIEWPORT: str
    EXECUTION_WHILE_NOT_RENDERED: str
    FOCUS_WITHOUT_USER_ACTIVATION: str
    FULLSCREEN: str
    FROBULATE: str
    GAMEPAD: str
    GEOLOCATION: str
    GYROSCOPE: str
    HID: str
    IDENTITY_CREDENTIALS_GET: str
    IDLE_DETECTION: str
    INTEREST_COHORT: str
    JOIN_AD_INTEREST_GROUP: str
    KEYBOARD_MAP: str
    LOCAL_FONTS: str
    MAGNETOMETER: str
    MICROPHONE: str
    MIDI: str
    OTP_CREDENTIALS: str
    PAYMENT: str
    PICTURE_IN_PICTURE: str
    PRIVATE_AGGREGATION: str
    PRIVATE_STATE_TOKEN_ISSUANCE: str
    PRIVATE_STATE_TOKEN_REDEMPTION: str
    PUBLICKEY_CREDENTIALS_CREATE: str
    PUBLICKEY_CREDENTIALS_GET: str
    RUN_AD_AUCTION: str
    SCREEN_WAKE_LOCK: str
    SERIAL: str
    SHARED_AUTOFILL: str
    SHARED_STORAGE: str
    SHARED_STORAGE_SELECT_URL: str
    SMART_CARD: str
    STORAGE_ACCESS: str
    SUB_APPS: str
    SYNC_XHR: str
    UNLOAD: str
    USB: str
    USB_UNRESTRICTED: str
    VERTICAL_SCROLL: str
    WEB_PRINTING: str
    WEB_SHARE: str
    WINDOW_MANAGEMENT: str
    WINDOW_PLACEMENT: str
    XR_SPATIAL_TRACKING: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PermissionsPolicyFeature: ...

class PermissionsPolicyBlockReason(enum.Enum):
    HEADER: str
    IFRAME_ATTRIBUTE: str
    IN_FENCED_FRAME_TREE: str
    IN_ISOLATED_APP: str
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
    def __init__(self, frame_id, block_reason) -> None: ...

@dataclass
class PermissionsPolicyFeatureState:
    feature: PermissionsPolicyFeature
    allowed: bool
    locator: typing.Optional[PermissionsPolicyBlockLocator] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PermissionsPolicyFeatureState: ...
    def __init__(self, feature, allowed, locator) -> None: ...

class OriginTrialTokenStatus(enum.Enum):
    SUCCESS: str
    NOT_SUPPORTED: str
    INSECURE: str
    EXPIRED: str
    WRONG_ORIGIN: str
    INVALID_SIGNATURE: str
    MALFORMED: str
    WRONG_VERSION: str
    FEATURE_DISABLED: str
    TOKEN_DISABLED: str
    FEATURE_DISABLED_FOR_USER: str
    UNKNOWN_TRIAL: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> OriginTrialTokenStatus: ...

class OriginTrialStatus(enum.Enum):
    ENABLED: str
    VALID_TOKEN_NOT_PROVIDED: str
    OS_NOT_SUPPORTED: str
    TRIAL_NOT_ALLOWED: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> OriginTrialStatus: ...

class OriginTrialUsageRestriction(enum.Enum):
    NONE: str
    SUBSET: str
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
    def __init__(self, origin, match_sub_domains, trial_name, expiry_time, is_third_party, usage_restriction) -> None: ...

@dataclass
class OriginTrialTokenWithStatus:
    raw_token_text: str
    status: OriginTrialTokenStatus
    parsed_token: typing.Optional[OriginTrialToken] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> OriginTrialTokenWithStatus: ...
    def __init__(self, raw_token_text, status, parsed_token) -> None: ...

@dataclass
class OriginTrial:
    trial_name: str
    status: OriginTrialStatus
    tokens_with_status: typing.List[OriginTrialTokenWithStatus]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> OriginTrial: ...
    def __init__(self, trial_name, status, tokens_with_status) -> None: ...

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
    gated_api_features: typing.List[GatedAPIFeatures]
    parent_id: typing.Optional[FrameId] = ...
    name: typing.Optional[str] = ...
    url_fragment: typing.Optional[str] = ...
    unreachable_url: typing.Optional[str] = ...
    ad_frame_status: typing.Optional[AdFrameStatus] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Frame: ...
    def __init__(self, id_, loader_id, url, domain_and_registry, security_origin, mime_type, secure_context_type, cross_origin_isolated_context_type, gated_api_features, parent_id, name, url_fragment, unreachable_url, ad_frame_status) -> None: ...

@dataclass
class FrameResource:
    url: str
    type_: network.ResourceType
    mime_type: str
    last_modified: typing.Optional[network.TimeSinceEpoch] = ...
    content_size: typing.Optional[float] = ...
    failed: typing.Optional[bool] = ...
    canceled: typing.Optional[bool] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameResource: ...
    def __init__(self, url, type_, mime_type, last_modified, content_size, failed, canceled) -> None: ...

@dataclass
class FrameResourceTree:
    frame: Frame
    resources: typing.List[FrameResource]
    child_frames: typing.Optional[typing.List[FrameResourceTree]] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameResourceTree: ...
    def __init__(self, frame, resources, child_frames) -> None: ...

@dataclass
class FrameTree:
    frame: Frame
    child_frames: typing.Optional[typing.List[FrameTree]] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameTree: ...
    def __init__(self, frame, child_frames) -> None: ...

class ScriptIdentifier(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ScriptIdentifier: ...

class TransitionType(enum.Enum):
    LINK: str
    TYPED: str
    ADDRESS_BAR: str
    AUTO_BOOKMARK: str
    AUTO_SUBFRAME: str
    MANUAL_SUBFRAME: str
    GENERATED: str
    AUTO_TOPLEVEL: str
    FORM_SUBMIT: str
    RELOAD: str
    KEYWORD: str
    KEYWORD_GENERATED: str
    OTHER: str
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
    def __init__(self, id_, url, user_typed_url, title, transition_type) -> None: ...

@dataclass
class ScreencastFrameMetadata:
    offset_top: float
    page_scale_factor: float
    device_width: float
    device_height: float
    scroll_offset_x: float
    scroll_offset_y: float
    timestamp: typing.Optional[network.TimeSinceEpoch] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScreencastFrameMetadata: ...
    def __init__(self, offset_top, page_scale_factor, device_width, device_height, scroll_offset_x, scroll_offset_y, timestamp) -> None: ...

class DialogType(enum.Enum):
    ALERT: str
    CONFIRM: str
    PROMPT: str
    BEFOREUNLOAD: str
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
    def __init__(self, message, critical, line, column) -> None: ...

@dataclass
class AppManifestParsedProperties:
    scope: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AppManifestParsedProperties: ...
    def __init__(self, scope) -> None: ...

@dataclass
class LayoutViewport:
    page_x: int
    page_y: int
    client_width: int
    client_height: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LayoutViewport: ...
    def __init__(self, page_x, page_y, client_width, client_height) -> None: ...

@dataclass
class VisualViewport:
    offset_x: float
    offset_y: float
    page_x: float
    page_y: float
    client_width: float
    client_height: float
    scale: float
    zoom: typing.Optional[float] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> VisualViewport: ...
    def __init__(self, offset_x, offset_y, page_x, page_y, client_width, client_height, scale, zoom) -> None: ...

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
    def __init__(self, x, y, width, height, scale) -> None: ...

@dataclass
class FontFamilies:
    standard: typing.Optional[str] = ...
    fixed: typing.Optional[str] = ...
    serif: typing.Optional[str] = ...
    sans_serif: typing.Optional[str] = ...
    cursive: typing.Optional[str] = ...
    fantasy: typing.Optional[str] = ...
    math: typing.Optional[str] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FontFamilies: ...
    def __init__(self, standard, fixed, serif, sans_serif, cursive, fantasy, math) -> None: ...

@dataclass
class ScriptFontFamilies:
    script: str
    font_families: FontFamilies
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScriptFontFamilies: ...
    def __init__(self, script, font_families) -> None: ...

@dataclass
class FontSizes:
    standard: typing.Optional[int] = ...
    fixed: typing.Optional[int] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FontSizes: ...
    def __init__(self, standard, fixed) -> None: ...

class ClientNavigationReason(enum.Enum):
    FORM_SUBMISSION_GET: str
    FORM_SUBMISSION_POST: str
    HTTP_HEADER_REFRESH: str
    SCRIPT_INITIATED: str
    META_TAG_REFRESH: str
    PAGE_BLOCK_INTERSTITIAL: str
    RELOAD: str
    ANCHOR_CLICK: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ClientNavigationReason: ...

class ClientNavigationDisposition(enum.Enum):
    CURRENT_TAB: str
    NEW_TAB: str
    NEW_WINDOW: str
    DOWNLOAD: str
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
    def __init__(self, name, value) -> None: ...

@dataclass
class InstallabilityError:
    error_id: str
    error_arguments: typing.List[InstallabilityErrorArgument]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InstallabilityError: ...
    def __init__(self, error_id, error_arguments) -> None: ...

class ReferrerPolicy(enum.Enum):
    NO_REFERRER: str
    NO_REFERRER_WHEN_DOWNGRADE: str
    ORIGIN: str
    ORIGIN_WHEN_CROSS_ORIGIN: str
    SAME_ORIGIN: str
    STRICT_ORIGIN: str
    STRICT_ORIGIN_WHEN_CROSS_ORIGIN: str
    UNSAFE_URL: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ReferrerPolicy: ...

@dataclass
class CompilationCacheParams:
    url: str
    eager: typing.Optional[bool] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CompilationCacheParams: ...
    def __init__(self, url, eager) -> None: ...

class AutoResponseMode(enum.Enum):
    NONE: str
    AUTO_ACCEPT: str
    AUTO_REJECT: str
    AUTO_OPT_OUT: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AutoResponseMode: ...

class NavigationType(enum.Enum):
    NAVIGATION: str
    BACK_FORWARD_CACHE_RESTORE: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> NavigationType: ...

class BackForwardCacheNotRestoredReason(enum.Enum):
    NOT_PRIMARY_MAIN_FRAME: str
    BACK_FORWARD_CACHE_DISABLED: str
    RELATED_ACTIVE_CONTENTS_EXIST: str
    HTTP_STATUS_NOT_OK: str
    SCHEME_NOT_HTTP_OR_HTTPS: str
    LOADING: str
    WAS_GRANTED_MEDIA_ACCESS: str
    DISABLE_FOR_RENDER_FRAME_HOST_CALLED: str
    DOMAIN_NOT_ALLOWED: str
    HTTP_METHOD_NOT_GET: str
    SUBFRAME_IS_NAVIGATING: str
    TIMEOUT: str
    CACHE_LIMIT: str
    JAVA_SCRIPT_EXECUTION: str
    RENDERER_PROCESS_KILLED: str
    RENDERER_PROCESS_CRASHED: str
    SCHEDULER_TRACKED_FEATURE_USED: str
    CONFLICTING_BROWSING_INSTANCE: str
    CACHE_FLUSHED: str
    SERVICE_WORKER_VERSION_ACTIVATION: str
    SESSION_RESTORED: str
    SERVICE_WORKER_POST_MESSAGE: str
    ENTERED_BACK_FORWARD_CACHE_BEFORE_SERVICE_WORKER_HOST_ADDED: str
    RENDER_FRAME_HOST_REUSED_SAME_SITE: str
    RENDER_FRAME_HOST_REUSED_CROSS_SITE: str
    SERVICE_WORKER_CLAIM: str
    IGNORE_EVENT_AND_EVICT: str
    HAVE_INNER_CONTENTS: str
    TIMEOUT_PUTTING_IN_CACHE: str
    BACK_FORWARD_CACHE_DISABLED_BY_LOW_MEMORY: str
    BACK_FORWARD_CACHE_DISABLED_BY_COMMAND_LINE: str
    NETWORK_REQUEST_DATAPIPE_DRAINED_AS_BYTES_CONSUMER: str
    NETWORK_REQUEST_REDIRECTED: str
    NETWORK_REQUEST_TIMEOUT: str
    NETWORK_EXCEEDS_BUFFER_LIMIT: str
    NAVIGATION_CANCELLED_WHILE_RESTORING: str
    NOT_MOST_RECENT_NAVIGATION_ENTRY: str
    BACK_FORWARD_CACHE_DISABLED_FOR_PRERENDER: str
    USER_AGENT_OVERRIDE_DIFFERS: str
    FOREGROUND_CACHE_LIMIT: str
    BROWSING_INSTANCE_NOT_SWAPPED: str
    BACK_FORWARD_CACHE_DISABLED_FOR_DELEGATE: str
    UNLOAD_HANDLER_EXISTS_IN_MAIN_FRAME: str
    UNLOAD_HANDLER_EXISTS_IN_SUB_FRAME: str
    SERVICE_WORKER_UNREGISTRATION: str
    CACHE_CONTROL_NO_STORE: str
    CACHE_CONTROL_NO_STORE_COOKIE_MODIFIED: str
    CACHE_CONTROL_NO_STORE_HTTP_ONLY_COOKIE_MODIFIED: str
    NO_RESPONSE_HEAD: str
    UNKNOWN: str
    ACTIVATION_NAVIGATIONS_DISALLOWED_FOR_BUG1234857: str
    ERROR_DOCUMENT: str
    FENCED_FRAMES_EMBEDDER: str
    COOKIE_DISABLED: str
    HTTP_AUTH_REQUIRED: str
    COOKIE_FLUSHED: str
    WEB_SOCKET: str
    WEB_TRANSPORT: str
    WEB_RTC: str
    MAIN_RESOURCE_HAS_CACHE_CONTROL_NO_STORE: str
    MAIN_RESOURCE_HAS_CACHE_CONTROL_NO_CACHE: str
    SUBRESOURCE_HAS_CACHE_CONTROL_NO_STORE: str
    SUBRESOURCE_HAS_CACHE_CONTROL_NO_CACHE: str
    CONTAINS_PLUGINS: str
    DOCUMENT_LOADED: str
    DEDICATED_WORKER_OR_WORKLET: str
    OUTSTANDING_NETWORK_REQUEST_OTHERS: str
    REQUESTED_MIDI_PERMISSION: str
    REQUESTED_AUDIO_CAPTURE_PERMISSION: str
    REQUESTED_VIDEO_CAPTURE_PERMISSION: str
    REQUESTED_BACK_FORWARD_CACHE_BLOCKED_SENSORS: str
    REQUESTED_BACKGROUND_WORK_PERMISSION: str
    BROADCAST_CHANNEL: str
    WEB_XR: str
    SHARED_WORKER: str
    WEB_LOCKS: str
    WEB_HID: str
    WEB_SHARE: str
    REQUESTED_STORAGE_ACCESS_GRANT: str
    WEB_NFC: str
    OUTSTANDING_NETWORK_REQUEST_FETCH: str
    OUTSTANDING_NETWORK_REQUEST_XHR: str
    APP_BANNER: str
    PRINTING: str
    WEB_DATABASE: str
    PICTURE_IN_PICTURE: str
    PORTAL: str
    SPEECH_RECOGNIZER: str
    IDLE_MANAGER: str
    PAYMENT_MANAGER: str
    SPEECH_SYNTHESIS: str
    KEYBOARD_LOCK: str
    WEB_OTP_SERVICE: str
    OUTSTANDING_NETWORK_REQUEST_DIRECT_SOCKET: str
    INJECTED_JAVASCRIPT: str
    INJECTED_STYLE_SHEET: str
    KEEPALIVE_REQUEST: str
    INDEXED_DB_EVENT: str
    DUMMY: str
    JS_NETWORK_REQUEST_RECEIVED_CACHE_CONTROL_NO_STORE_RESOURCE: str
    WEB_RTC_STICKY: str
    WEB_TRANSPORT_STICKY: str
    WEB_SOCKET_STICKY: str
    SMART_CARD: str
    LIVE_MEDIA_STREAM_TRACK: str
    CONTENT_SECURITY_HANDLER: str
    CONTENT_WEB_AUTHENTICATION_API: str
    CONTENT_FILE_CHOOSER: str
    CONTENT_SERIAL: str
    CONTENT_FILE_SYSTEM_ACCESS: str
    CONTENT_MEDIA_DEVICES_DISPATCHER_HOST: str
    CONTENT_WEB_BLUETOOTH: str
    CONTENT_WEB_USB: str
    CONTENT_MEDIA_SESSION_SERVICE: str
    CONTENT_SCREEN_READER: str
    EMBEDDER_POPUP_BLOCKER_TAB_HELPER: str
    EMBEDDER_SAFE_BROWSING_TRIGGERED_POPUP_BLOCKER: str
    EMBEDDER_SAFE_BROWSING_THREAT_DETAILS: str
    EMBEDDER_APP_BANNER_MANAGER: str
    EMBEDDER_DOM_DISTILLER_VIEWER_SOURCE: str
    EMBEDDER_DOM_DISTILLER_SELF_DELETING_REQUEST_DELEGATE: str
    EMBEDDER_OOM_INTERVENTION_TAB_HELPER: str
    EMBEDDER_OFFLINE_PAGE: str
    EMBEDDER_CHROME_PASSWORD_MANAGER_CLIENT_BIND_CREDENTIAL_MANAGER: str
    EMBEDDER_PERMISSION_REQUEST_MANAGER: str
    EMBEDDER_MODAL_DIALOG: str
    EMBEDDER_EXTENSIONS: str
    EMBEDDER_EXTENSION_MESSAGING: str
    EMBEDDER_EXTENSION_MESSAGING_FOR_OPEN_PORT: str
    EMBEDDER_EXTENSION_SENT_MESSAGE_TO_CACHED_FRAME: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> BackForwardCacheNotRestoredReason: ...

class BackForwardCacheNotRestoredReasonType(enum.Enum):
    SUPPORT_PENDING: str
    PAGE_SUPPORT_NEEDED: str
    CIRCUMSTANTIAL: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> BackForwardCacheNotRestoredReasonType: ...

@dataclass
class BackForwardCacheBlockingDetails:
    line_number: int
    column_number: int
    url: typing.Optional[str] = ...
    function: typing.Optional[str] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackForwardCacheBlockingDetails: ...
    def __init__(self, line_number, column_number, url, function) -> None: ...

@dataclass
class BackForwardCacheNotRestoredExplanation:
    type_: BackForwardCacheNotRestoredReasonType
    reason: BackForwardCacheNotRestoredReason
    context: typing.Optional[str] = ...
    details: typing.Optional[typing.List[BackForwardCacheBlockingDetails]] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackForwardCacheNotRestoredExplanation: ...
    def __init__(self, type_, reason, context, details) -> None: ...

@dataclass
class BackForwardCacheNotRestoredExplanationTree:
    url: str
    explanations: typing.List[BackForwardCacheNotRestoredExplanation]
    children: typing.List[BackForwardCacheNotRestoredExplanationTree]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackForwardCacheNotRestoredExplanationTree: ...
    def __init__(self, url, explanations, children) -> None: ...

def add_script_to_evaluate_on_load(script_source: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, ScriptIdentifier]: ...
def add_script_to_evaluate_on_new_document(source: str, world_name: typing.Optional[str] = None, include_command_line_api: typing.Optional[bool] = None, run_immediately: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, ScriptIdentifier]: ...
def bring_to_front() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def capture_screenshot(format_: typing.Optional[str] = None, quality: typing.Optional[int] = None, clip: typing.Optional[Viewport] = None, from_surface: typing.Optional[bool] = None, capture_beyond_viewport: typing.Optional[bool] = None, optimize_for_speed: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, str]: ...
def capture_snapshot(format_: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, str]: ...
def clear_device_metrics_override() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_device_orientation_override() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_geolocation_override() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def create_isolated_world(frame_id: FrameId, world_name: typing.Optional[str] = None, grant_univeral_access: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, runtime.ExecutionContextId]: ...
def delete_cookie(cookie_name: str, url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_app_manifest() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[str, typing.List[AppManifestError], typing.Optional[str], typing.Optional[AppManifestParsedProperties]]]: ...
def get_installability_errors() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[InstallabilityError]]: ...
def get_manifest_icons() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Optional[str]]: ...
def get_app_id() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[typing.Optional[str], typing.Optional[str]]]: ...
def get_ad_script_id(frame_id: FrameId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Optional[AdScriptId]]: ...
def get_frame_tree() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, FrameTree]: ...
def get_layout_metrics() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[LayoutViewport, VisualViewport, dom.Rect, LayoutViewport, VisualViewport, dom.Rect]]: ...
def get_navigation_history() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[int, typing.List[NavigationEntry]]]: ...
def reset_navigation_history() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_resource_content(frame_id: FrameId, url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[str, bool]]: ...
def get_resource_tree() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, FrameResourceTree]: ...
def handle_java_script_dialog(accept: bool, prompt_text: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def navigate(url: str, referrer: typing.Optional[str] = None, transition_type: typing.Optional[TransitionType] = None, frame_id: typing.Optional[FrameId] = None, referrer_policy: typing.Optional[ReferrerPolicy] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[FrameId, typing.Optional[network.LoaderId], typing.Optional[str]]]: ...
def navigate_to_history_entry(entry_id: int) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def print_to_pdf(landscape: typing.Optional[bool] = None, display_header_footer: typing.Optional[bool] = None, print_background: typing.Optional[bool] = None, scale: typing.Optional[float] = None, paper_width: typing.Optional[float] = None, paper_height: typing.Optional[float] = None, margin_top: typing.Optional[float] = None, margin_bottom: typing.Optional[float] = None, margin_left: typing.Optional[float] = None, margin_right: typing.Optional[float] = None, page_ranges: typing.Optional[str] = None, header_template: typing.Optional[str] = None, footer_template: typing.Optional[str] = None, prefer_css_page_size: typing.Optional[bool] = None, transfer_mode: typing.Optional[str] = None, generate_tagged_pdf: typing.Optional[bool] = None, generate_document_outline: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[str, typing.Optional[io.StreamHandle]]]: ...
def reload(ignore_cache: typing.Optional[bool] = None, script_to_evaluate_on_load: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def remove_script_to_evaluate_on_load(identifier: ScriptIdentifier) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def remove_script_to_evaluate_on_new_document(identifier: ScriptIdentifier) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def screencast_frame_ack(session_id: int) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def search_in_resource(frame_id: FrameId, url: str, query: str, case_sensitive: typing.Optional[bool] = None, is_regex: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[debugger.SearchMatch]]: ...
def set_ad_blocking_enabled(enabled: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_bypass_csp(enabled: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_permissions_policy_state(frame_id: FrameId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[PermissionsPolicyFeatureState]]: ...
def get_origin_trials(frame_id: FrameId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[OriginTrial]]: ...
def set_device_metrics_override(width: int, height: int, device_scale_factor: float, mobile: bool, scale: typing.Optional[float] = None, screen_width: typing.Optional[int] = None, screen_height: typing.Optional[int] = None, position_x: typing.Optional[int] = None, position_y: typing.Optional[int] = None, dont_set_visible_size: typing.Optional[bool] = None, screen_orientation: typing.Optional[emulation.ScreenOrientation] = None, viewport: typing.Optional[Viewport] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_device_orientation_override(alpha: float, beta: float, gamma: float) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_font_families(font_families: FontFamilies, for_scripts: typing.Optional[typing.List[ScriptFontFamilies]] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_font_sizes(font_sizes: FontSizes) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_document_content(frame_id: FrameId, html: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_download_behavior(behavior: str, download_path: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_geolocation_override(latitude: typing.Optional[float] = None, longitude: typing.Optional[float] = None, accuracy: typing.Optional[float] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_lifecycle_events_enabled(enabled: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_touch_emulation_enabled(enabled: bool, configuration: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def start_screencast(format_: typing.Optional[str] = None, quality: typing.Optional[int] = None, max_width: typing.Optional[int] = None, max_height: typing.Optional[int] = None, every_nth_frame: typing.Optional[int] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def stop_loading() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def crash() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def close() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_web_lifecycle_state(state: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def stop_screencast() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def produce_compilation_cache(scripts: typing.List[CompilationCacheParams]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def add_compilation_cache(url: str, data: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_compilation_cache() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_spc_transaction_mode(mode: AutoResponseMode) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_rph_registration_mode(mode: AutoResponseMode) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def generate_test_report(message: str, group: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def wait_for_debugger() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_intercept_file_chooser_dialog(enabled: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_prerendering_allowed(is_allowed: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class DomContentEventFired:
    timestamp: network.MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DomContentEventFired: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, timestamp) -> None: ...

@dataclass
class FileChooserOpened:
    frame_id: FrameId
    mode: str
    backend_node_id: typing.Optional[dom.BackendNodeId]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FileChooserOpened: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id, mode, backend_node_id) -> None: ...

@dataclass
class FrameAttached:
    frame_id: FrameId
    parent_frame_id: FrameId
    stack: typing.Optional[runtime.StackTrace]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameAttached: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id, parent_frame_id, stack) -> None: ...

@dataclass
class FrameClearedScheduledNavigation:
    frame_id: FrameId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameClearedScheduledNavigation: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id) -> None: ...

@dataclass
class FrameDetached:
    frame_id: FrameId
    reason: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameDetached: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id, reason) -> None: ...

@dataclass
class FrameNavigated:
    frame: Frame
    type_: NavigationType
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameNavigated: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame, type_) -> None: ...

@dataclass
class DocumentOpened:
    frame: Frame
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DocumentOpened: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame) -> None: ...

@dataclass
class FrameResized:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameResized: ...
    def to_json(self) -> T_JSON_DICT: ...

@dataclass
class FrameRequestedNavigation:
    frame_id: FrameId
    reason: ClientNavigationReason
    url: str
    disposition: ClientNavigationDisposition
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameRequestedNavigation: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id, reason, url, disposition) -> None: ...

@dataclass
class FrameScheduledNavigation:
    frame_id: FrameId
    delay: float
    reason: ClientNavigationReason
    url: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameScheduledNavigation: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id, delay, reason, url) -> None: ...

@dataclass
class FrameStartedLoading:
    frame_id: FrameId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameStartedLoading: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id) -> None: ...

@dataclass
class FrameStoppedLoading:
    frame_id: FrameId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FrameStoppedLoading: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id) -> None: ...

@dataclass
class DownloadWillBegin:
    frame_id: FrameId
    guid: str
    url: str
    suggested_filename: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DownloadWillBegin: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id, guid, url, suggested_filename) -> None: ...

@dataclass
class DownloadProgress:
    guid: str
    total_bytes: float
    received_bytes: float
    state: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DownloadProgress: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, guid, total_bytes, received_bytes, state) -> None: ...

@dataclass
class InterstitialHidden:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InterstitialHidden: ...
    def to_json(self) -> T_JSON_DICT: ...

@dataclass
class InterstitialShown:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InterstitialShown: ...
    def to_json(self) -> T_JSON_DICT: ...

@dataclass
class JavascriptDialogClosed:
    result: bool
    user_input: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> JavascriptDialogClosed: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, result, user_input) -> None: ...

@dataclass
class JavascriptDialogOpening:
    url: str
    message: str
    type_: DialogType
    has_browser_handler: bool
    default_prompt: typing.Optional[str]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> JavascriptDialogOpening: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, url, message, type_, has_browser_handler, default_prompt) -> None: ...

@dataclass
class LifecycleEvent:
    frame_id: FrameId
    loader_id: network.LoaderId
    name: str
    timestamp: network.MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LifecycleEvent: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id, loader_id, name, timestamp) -> None: ...

@dataclass
class BackForwardCacheNotUsed:
    loader_id: network.LoaderId
    frame_id: FrameId
    not_restored_explanations: typing.List[BackForwardCacheNotRestoredExplanation]
    not_restored_explanations_tree: typing.Optional[BackForwardCacheNotRestoredExplanationTree]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackForwardCacheNotUsed: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, loader_id, frame_id, not_restored_explanations, not_restored_explanations_tree) -> None: ...

@dataclass
class LoadEventFired:
    timestamp: network.MonotonicTime
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LoadEventFired: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, timestamp) -> None: ...

@dataclass
class NavigatedWithinDocument:
    frame_id: FrameId
    url: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> NavigatedWithinDocument: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, frame_id, url) -> None: ...

@dataclass
class ScreencastFrame:
    data: str
    metadata: ScreencastFrameMetadata
    session_id: int
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScreencastFrame: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, data, metadata, session_id) -> None: ...

@dataclass
class ScreencastVisibilityChanged:
    visible: bool
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScreencastVisibilityChanged: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, visible) -> None: ...

@dataclass
class WindowOpen:
    url: str
    window_name: str
    window_features: typing.List[str]
    user_gesture: bool
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WindowOpen: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, url, window_name, window_features, user_gesture) -> None: ...

@dataclass
class CompilationCacheProduced:
    url: str
    data: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CompilationCacheProduced: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, url, data) -> None: ...
