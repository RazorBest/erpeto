import enum
import typing
from . import dom as dom, network as network, page as page
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class RuleSetId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> RuleSetId: ...

@dataclass
class RuleSet:
    id_: RuleSetId
    loader_id: network.LoaderId
    source_text: str
    backend_node_id: typing.Optional[dom.BackendNodeId] = ...
    url: typing.Optional[str] = ...
    request_id: typing.Optional[network.RequestId] = ...
    error_type: typing.Optional[RuleSetErrorType] = ...
    error_message: typing.Optional[str] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RuleSet: ...
    def __init__(self, id_, loader_id, source_text, backend_node_id, url, request_id, error_type, error_message) -> None: ...

class RuleSetErrorType(enum.Enum):
    SOURCE_IS_NOT_JSON_OBJECT: str
    INVALID_RULES_SKIPPED: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> RuleSetErrorType: ...

class SpeculationAction(enum.Enum):
    PREFETCH: str
    PRERENDER: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SpeculationAction: ...

class SpeculationTargetHint(enum.Enum):
    BLANK: str
    SELF: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SpeculationTargetHint: ...

@dataclass
class PreloadingAttemptKey:
    loader_id: network.LoaderId
    action: SpeculationAction
    url: str
    target_hint: typing.Optional[SpeculationTargetHint] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PreloadingAttemptKey: ...
    def __init__(self, loader_id, action, url, target_hint) -> None: ...

@dataclass
class PreloadingAttemptSource:
    key: PreloadingAttemptKey
    rule_set_ids: typing.List[RuleSetId]
    node_ids: typing.List[dom.BackendNodeId]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PreloadingAttemptSource: ...
    def __init__(self, key, rule_set_ids, node_ids) -> None: ...

class PrerenderFinalStatus(enum.Enum):
    ACTIVATED: str
    DESTROYED: str
    LOW_END_DEVICE: str
    INVALID_SCHEME_REDIRECT: str
    INVALID_SCHEME_NAVIGATION: str
    NAVIGATION_REQUEST_BLOCKED_BY_CSP: str
    MAIN_FRAME_NAVIGATION: str
    MOJO_BINDER_POLICY: str
    RENDERER_PROCESS_CRASHED: str
    RENDERER_PROCESS_KILLED: str
    DOWNLOAD: str
    TRIGGER_DESTROYED: str
    NAVIGATION_NOT_COMMITTED: str
    NAVIGATION_BAD_HTTP_STATUS: str
    CLIENT_CERT_REQUESTED: str
    NAVIGATION_REQUEST_NETWORK_ERROR: str
    CANCEL_ALL_HOSTS_FOR_TESTING: str
    DID_FAIL_LOAD: str
    STOP: str
    SSL_CERTIFICATE_ERROR: str
    LOGIN_AUTH_REQUESTED: str
    UA_CHANGE_REQUIRES_RELOAD: str
    BLOCKED_BY_CLIENT: str
    AUDIO_OUTPUT_DEVICE_REQUESTED: str
    MIXED_CONTENT: str
    TRIGGER_BACKGROUNDED: str
    MEMORY_LIMIT_EXCEEDED: str
    DATA_SAVER_ENABLED: str
    TRIGGER_URL_HAS_EFFECTIVE_URL: str
    ACTIVATED_BEFORE_STARTED: str
    INACTIVE_PAGE_RESTRICTION: str
    START_FAILED: str
    TIMEOUT_BACKGROUNDED: str
    CROSS_SITE_REDIRECT_IN_INITIAL_NAVIGATION: str
    CROSS_SITE_NAVIGATION_IN_INITIAL_NAVIGATION: str
    SAME_SITE_CROSS_ORIGIN_REDIRECT_NOT_OPT_IN_IN_INITIAL_NAVIGATION: str
    SAME_SITE_CROSS_ORIGIN_NAVIGATION_NOT_OPT_IN_IN_INITIAL_NAVIGATION: str
    ACTIVATION_NAVIGATION_PARAMETER_MISMATCH: str
    ACTIVATED_IN_BACKGROUND: str
    EMBEDDER_HOST_DISALLOWED: str
    ACTIVATION_NAVIGATION_DESTROYED_BEFORE_SUCCESS: str
    TAB_CLOSED_BY_USER_GESTURE: str
    TAB_CLOSED_WITHOUT_USER_GESTURE: str
    PRIMARY_MAIN_FRAME_RENDERER_PROCESS_CRASHED: str
    PRIMARY_MAIN_FRAME_RENDERER_PROCESS_KILLED: str
    ACTIVATION_FRAME_POLICY_NOT_COMPATIBLE: str
    PRELOADING_DISABLED: str
    BATTERY_SAVER_ENABLED: str
    ACTIVATED_DURING_MAIN_FRAME_NAVIGATION: str
    PRELOADING_UNSUPPORTED_BY_WEB_CONTENTS: str
    CROSS_SITE_REDIRECT_IN_MAIN_FRAME_NAVIGATION: str
    CROSS_SITE_NAVIGATION_IN_MAIN_FRAME_NAVIGATION: str
    SAME_SITE_CROSS_ORIGIN_REDIRECT_NOT_OPT_IN_IN_MAIN_FRAME_NAVIGATION: str
    SAME_SITE_CROSS_ORIGIN_NAVIGATION_NOT_OPT_IN_IN_MAIN_FRAME_NAVIGATION: str
    MEMORY_PRESSURE_ON_TRIGGER: str
    MEMORY_PRESSURE_AFTER_TRIGGERED: str
    PRERENDERING_DISABLED_BY_DEV_TOOLS: str
    SPECULATION_RULE_REMOVED: str
    ACTIVATED_WITH_AUXILIARY_BROWSING_CONTEXTS: str
    MAX_NUM_OF_RUNNING_EAGER_PRERENDERS_EXCEEDED: str
    MAX_NUM_OF_RUNNING_NON_EAGER_PRERENDERS_EXCEEDED: str
    MAX_NUM_OF_RUNNING_EMBEDDER_PRERENDERS_EXCEEDED: str
    PRERENDERING_URL_HAS_EFFECTIVE_URL: str
    REDIRECTED_PRERENDERING_URL_HAS_EFFECTIVE_URL: str
    ACTIVATION_URL_HAS_EFFECTIVE_URL: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PrerenderFinalStatus: ...

class PreloadingStatus(enum.Enum):
    PENDING: str
    RUNNING: str
    READY: str
    SUCCESS: str
    FAILURE: str
    NOT_SUPPORTED: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PreloadingStatus: ...

class PrefetchStatus(enum.Enum):
    PREFETCH_ALLOWED: str
    PREFETCH_FAILED_INELIGIBLE_REDIRECT: str
    PREFETCH_FAILED_INVALID_REDIRECT: str
    PREFETCH_FAILED_MIME_NOT_SUPPORTED: str
    PREFETCH_FAILED_NET_ERROR: str
    PREFETCH_FAILED_NON2_XX: str
    PREFETCH_FAILED_PER_PAGE_LIMIT_EXCEEDED: str
    PREFETCH_EVICTED_AFTER_CANDIDATE_REMOVED: str
    PREFETCH_EVICTED_FOR_NEWER_PREFETCH: str
    PREFETCH_HELDBACK: str
    PREFETCH_INELIGIBLE_RETRY_AFTER: str
    PREFETCH_IS_PRIVACY_DECOY: str
    PREFETCH_IS_STALE: str
    PREFETCH_NOT_ELIGIBLE_BROWSER_CONTEXT_OFF_THE_RECORD: str
    PREFETCH_NOT_ELIGIBLE_DATA_SAVER_ENABLED: str
    PREFETCH_NOT_ELIGIBLE_EXISTING_PROXY: str
    PREFETCH_NOT_ELIGIBLE_HOST_IS_NON_UNIQUE: str
    PREFETCH_NOT_ELIGIBLE_NON_DEFAULT_STORAGE_PARTITION: str
    PREFETCH_NOT_ELIGIBLE_SAME_SITE_CROSS_ORIGIN_PREFETCH_REQUIRED_PROXY: str
    PREFETCH_NOT_ELIGIBLE_SCHEME_IS_NOT_HTTPS: str
    PREFETCH_NOT_ELIGIBLE_USER_HAS_COOKIES: str
    PREFETCH_NOT_ELIGIBLE_USER_HAS_SERVICE_WORKER: str
    PREFETCH_NOT_ELIGIBLE_BATTERY_SAVER_ENABLED: str
    PREFETCH_NOT_ELIGIBLE_PRELOADING_DISABLED: str
    PREFETCH_NOT_FINISHED_IN_TIME: str
    PREFETCH_NOT_STARTED: str
    PREFETCH_NOT_USED_COOKIES_CHANGED: str
    PREFETCH_PROXY_NOT_AVAILABLE: str
    PREFETCH_RESPONSE_USED: str
    PREFETCH_SUCCESSFUL_BUT_NOT_USED: str
    PREFETCH_NOT_USED_PROBE_FAILED: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PrefetchStatus: ...

@dataclass
class PrerenderMismatchedHeaders:
    header_name: str
    initial_value: typing.Optional[str] = ...
    activation_value: typing.Optional[str] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PrerenderMismatchedHeaders: ...
    def __init__(self, header_name, initial_value, activation_value) -> None: ...

def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class RuleSetUpdated:
    rule_set: RuleSet
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RuleSetUpdated: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, rule_set) -> None: ...

@dataclass
class RuleSetRemoved:
    id_: RuleSetId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RuleSetRemoved: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, id_) -> None: ...

@dataclass
class PreloadEnabledStateUpdated:
    disabled_by_preference: bool
    disabled_by_data_saver: bool
    disabled_by_battery_saver: bool
    disabled_by_holdback_prefetch_speculation_rules: bool
    disabled_by_holdback_prerender_speculation_rules: bool
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PreloadEnabledStateUpdated: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, disabled_by_preference, disabled_by_data_saver, disabled_by_battery_saver, disabled_by_holdback_prefetch_speculation_rules, disabled_by_holdback_prerender_speculation_rules) -> None: ...

@dataclass
class PrefetchStatusUpdated:
    key: PreloadingAttemptKey
    initiating_frame_id: page.FrameId
    prefetch_url: str
    status: PreloadingStatus
    prefetch_status: PrefetchStatus
    request_id: network.RequestId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PrefetchStatusUpdated: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, key, initiating_frame_id, prefetch_url, status, prefetch_status, request_id) -> None: ...

@dataclass
class PrerenderStatusUpdated:
    key: PreloadingAttemptKey
    status: PreloadingStatus
    prerender_status: typing.Optional[PrerenderFinalStatus]
    disallowed_mojo_interface: typing.Optional[str]
    mismatched_headers: typing.Optional[typing.List[PrerenderMismatchedHeaders]]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PrerenderStatusUpdated: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, key, status, prerender_status, disallowed_mojo_interface, mismatched_headers) -> None: ...

@dataclass
class PreloadingAttemptSourcesUpdated:
    loader_id: network.LoaderId
    preloading_attempt_sources: typing.List[PreloadingAttemptSource]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PreloadingAttemptSourcesUpdated: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, loader_id, preloading_attempt_sources) -> None: ...
