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
    backend_node_id: dom.BackendNodeId | None = ...
    url: str | None = ...
    request_id: network.RequestId | None = ...
    error_type: RuleSetErrorType | None = ...
    error_message: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RuleSet: ...

class RuleSetErrorType(enum.Enum):
    SOURCE_IS_NOT_JSON_OBJECT = 'SourceIsNotJsonObject'
    INVALID_RULES_SKIPPED = 'InvalidRulesSkipped'
    INVALID_RULESET_LEVEL_TAG = 'InvalidRulesetLevelTag'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> RuleSetErrorType: ...

class SpeculationAction(enum.Enum):
    PREFETCH = 'Prefetch'
    PRERENDER = 'Prerender'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SpeculationAction: ...

class SpeculationTargetHint(enum.Enum):
    BLANK = 'Blank'
    SELF = 'Self'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SpeculationTargetHint: ...

@dataclass
class PreloadingAttemptKey:
    loader_id: network.LoaderId
    action: SpeculationAction
    url: str
    target_hint: SpeculationTargetHint | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PreloadingAttemptKey: ...

@dataclass
class PreloadingAttemptSource:
    key: PreloadingAttemptKey
    rule_set_ids: list[RuleSetId]
    node_ids: list[dom.BackendNodeId]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PreloadingAttemptSource: ...

class PreloadPipelineId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PreloadPipelineId: ...

class PrerenderFinalStatus(enum.Enum):
    ACTIVATED = 'Activated'
    DESTROYED = 'Destroyed'
    LOW_END_DEVICE = 'LowEndDevice'
    INVALID_SCHEME_REDIRECT = 'InvalidSchemeRedirect'
    INVALID_SCHEME_NAVIGATION = 'InvalidSchemeNavigation'
    NAVIGATION_REQUEST_BLOCKED_BY_CSP = 'NavigationRequestBlockedByCsp'
    MOJO_BINDER_POLICY = 'MojoBinderPolicy'
    RENDERER_PROCESS_CRASHED = 'RendererProcessCrashed'
    RENDERER_PROCESS_KILLED = 'RendererProcessKilled'
    DOWNLOAD = 'Download'
    TRIGGER_DESTROYED = 'TriggerDestroyed'
    NAVIGATION_NOT_COMMITTED = 'NavigationNotCommitted'
    NAVIGATION_BAD_HTTP_STATUS = 'NavigationBadHttpStatus'
    CLIENT_CERT_REQUESTED = 'ClientCertRequested'
    NAVIGATION_REQUEST_NETWORK_ERROR = 'NavigationRequestNetworkError'
    CANCEL_ALL_HOSTS_FOR_TESTING = 'CancelAllHostsForTesting'
    DID_FAIL_LOAD = 'DidFailLoad'
    STOP = 'Stop'
    SSL_CERTIFICATE_ERROR = 'SslCertificateError'
    LOGIN_AUTH_REQUESTED = 'LoginAuthRequested'
    UA_CHANGE_REQUIRES_RELOAD = 'UaChangeRequiresReload'
    BLOCKED_BY_CLIENT = 'BlockedByClient'
    AUDIO_OUTPUT_DEVICE_REQUESTED = 'AudioOutputDeviceRequested'
    MIXED_CONTENT = 'MixedContent'
    TRIGGER_BACKGROUNDED = 'TriggerBackgrounded'
    MEMORY_LIMIT_EXCEEDED = 'MemoryLimitExceeded'
    DATA_SAVER_ENABLED = 'DataSaverEnabled'
    TRIGGER_URL_HAS_EFFECTIVE_URL = 'TriggerUrlHasEffectiveUrl'
    ACTIVATED_BEFORE_STARTED = 'ActivatedBeforeStarted'
    INACTIVE_PAGE_RESTRICTION = 'InactivePageRestriction'
    START_FAILED = 'StartFailed'
    TIMEOUT_BACKGROUNDED = 'TimeoutBackgrounded'
    CROSS_SITE_REDIRECT_IN_INITIAL_NAVIGATION = 'CrossSiteRedirectInInitialNavigation'
    CROSS_SITE_NAVIGATION_IN_INITIAL_NAVIGATION = 'CrossSiteNavigationInInitialNavigation'
    SAME_SITE_CROSS_ORIGIN_REDIRECT_NOT_OPT_IN_IN_INITIAL_NAVIGATION = 'SameSiteCrossOriginRedirectNotOptInInInitialNavigation'
    SAME_SITE_CROSS_ORIGIN_NAVIGATION_NOT_OPT_IN_IN_INITIAL_NAVIGATION = 'SameSiteCrossOriginNavigationNotOptInInInitialNavigation'
    ACTIVATION_NAVIGATION_PARAMETER_MISMATCH = 'ActivationNavigationParameterMismatch'
    ACTIVATED_IN_BACKGROUND = 'ActivatedInBackground'
    EMBEDDER_HOST_DISALLOWED = 'EmbedderHostDisallowed'
    ACTIVATION_NAVIGATION_DESTROYED_BEFORE_SUCCESS = 'ActivationNavigationDestroyedBeforeSuccess'
    TAB_CLOSED_BY_USER_GESTURE = 'TabClosedByUserGesture'
    TAB_CLOSED_WITHOUT_USER_GESTURE = 'TabClosedWithoutUserGesture'
    PRIMARY_MAIN_FRAME_RENDERER_PROCESS_CRASHED = 'PrimaryMainFrameRendererProcessCrashed'
    PRIMARY_MAIN_FRAME_RENDERER_PROCESS_KILLED = 'PrimaryMainFrameRendererProcessKilled'
    ACTIVATION_FRAME_POLICY_NOT_COMPATIBLE = 'ActivationFramePolicyNotCompatible'
    PRELOADING_DISABLED = 'PreloadingDisabled'
    BATTERY_SAVER_ENABLED = 'BatterySaverEnabled'
    ACTIVATED_DURING_MAIN_FRAME_NAVIGATION = 'ActivatedDuringMainFrameNavigation'
    PRELOADING_UNSUPPORTED_BY_WEB_CONTENTS = 'PreloadingUnsupportedByWebContents'
    CROSS_SITE_REDIRECT_IN_MAIN_FRAME_NAVIGATION = 'CrossSiteRedirectInMainFrameNavigation'
    CROSS_SITE_NAVIGATION_IN_MAIN_FRAME_NAVIGATION = 'CrossSiteNavigationInMainFrameNavigation'
    SAME_SITE_CROSS_ORIGIN_REDIRECT_NOT_OPT_IN_IN_MAIN_FRAME_NAVIGATION = 'SameSiteCrossOriginRedirectNotOptInInMainFrameNavigation'
    SAME_SITE_CROSS_ORIGIN_NAVIGATION_NOT_OPT_IN_IN_MAIN_FRAME_NAVIGATION = 'SameSiteCrossOriginNavigationNotOptInInMainFrameNavigation'
    MEMORY_PRESSURE_ON_TRIGGER = 'MemoryPressureOnTrigger'
    MEMORY_PRESSURE_AFTER_TRIGGERED = 'MemoryPressureAfterTriggered'
    PRERENDERING_DISABLED_BY_DEV_TOOLS = 'PrerenderingDisabledByDevTools'
    SPECULATION_RULE_REMOVED = 'SpeculationRuleRemoved'
    ACTIVATED_WITH_AUXILIARY_BROWSING_CONTEXTS = 'ActivatedWithAuxiliaryBrowsingContexts'
    MAX_NUM_OF_RUNNING_EAGER_PRERENDERS_EXCEEDED = 'MaxNumOfRunningEagerPrerendersExceeded'
    MAX_NUM_OF_RUNNING_NON_EAGER_PRERENDERS_EXCEEDED = 'MaxNumOfRunningNonEagerPrerendersExceeded'
    MAX_NUM_OF_RUNNING_EMBEDDER_PRERENDERS_EXCEEDED = 'MaxNumOfRunningEmbedderPrerendersExceeded'
    PRERENDERING_URL_HAS_EFFECTIVE_URL = 'PrerenderingUrlHasEffectiveUrl'
    REDIRECTED_PRERENDERING_URL_HAS_EFFECTIVE_URL = 'RedirectedPrerenderingUrlHasEffectiveUrl'
    ACTIVATION_URL_HAS_EFFECTIVE_URL = 'ActivationUrlHasEffectiveUrl'
    JAVA_SCRIPT_INTERFACE_ADDED = 'JavaScriptInterfaceAdded'
    JAVA_SCRIPT_INTERFACE_REMOVED = 'JavaScriptInterfaceRemoved'
    ALL_PRERENDERING_CANCELED = 'AllPrerenderingCanceled'
    WINDOW_CLOSED = 'WindowClosed'
    SLOW_NETWORK = 'SlowNetwork'
    OTHER_PRERENDERED_PAGE_ACTIVATED = 'OtherPrerenderedPageActivated'
    V8_OPTIMIZER_DISABLED = 'V8OptimizerDisabled'
    PRERENDER_FAILED_DURING_PREFETCH = 'PrerenderFailedDuringPrefetch'
    BROWSING_DATA_REMOVED = 'BrowsingDataRemoved'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PrerenderFinalStatus: ...

class PreloadingStatus(enum.Enum):
    PENDING = 'Pending'
    RUNNING = 'Running'
    READY = 'Ready'
    SUCCESS = 'Success'
    FAILURE = 'Failure'
    NOT_SUPPORTED = 'NotSupported'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PreloadingStatus: ...

class PrefetchStatus(enum.Enum):
    PREFETCH_ALLOWED = 'PrefetchAllowed'
    PREFETCH_FAILED_INELIGIBLE_REDIRECT = 'PrefetchFailedIneligibleRedirect'
    PREFETCH_FAILED_INVALID_REDIRECT = 'PrefetchFailedInvalidRedirect'
    PREFETCH_FAILED_MIME_NOT_SUPPORTED = 'PrefetchFailedMIMENotSupported'
    PREFETCH_FAILED_NET_ERROR = 'PrefetchFailedNetError'
    PREFETCH_FAILED_NON2_XX = 'PrefetchFailedNon2XX'
    PREFETCH_EVICTED_AFTER_BROWSING_DATA_REMOVED = 'PrefetchEvictedAfterBrowsingDataRemoved'
    PREFETCH_EVICTED_AFTER_CANDIDATE_REMOVED = 'PrefetchEvictedAfterCandidateRemoved'
    PREFETCH_EVICTED_FOR_NEWER_PREFETCH = 'PrefetchEvictedForNewerPrefetch'
    PREFETCH_HELDBACK = 'PrefetchHeldback'
    PREFETCH_INELIGIBLE_RETRY_AFTER = 'PrefetchIneligibleRetryAfter'
    PREFETCH_IS_PRIVACY_DECOY = 'PrefetchIsPrivacyDecoy'
    PREFETCH_IS_STALE = 'PrefetchIsStale'
    PREFETCH_NOT_ELIGIBLE_BROWSER_CONTEXT_OFF_THE_RECORD = 'PrefetchNotEligibleBrowserContextOffTheRecord'
    PREFETCH_NOT_ELIGIBLE_DATA_SAVER_ENABLED = 'PrefetchNotEligibleDataSaverEnabled'
    PREFETCH_NOT_ELIGIBLE_EXISTING_PROXY = 'PrefetchNotEligibleExistingProxy'
    PREFETCH_NOT_ELIGIBLE_HOST_IS_NON_UNIQUE = 'PrefetchNotEligibleHostIsNonUnique'
    PREFETCH_NOT_ELIGIBLE_NON_DEFAULT_STORAGE_PARTITION = 'PrefetchNotEligibleNonDefaultStoragePartition'
    PREFETCH_NOT_ELIGIBLE_SAME_SITE_CROSS_ORIGIN_PREFETCH_REQUIRED_PROXY = 'PrefetchNotEligibleSameSiteCrossOriginPrefetchRequiredProxy'
    PREFETCH_NOT_ELIGIBLE_SCHEME_IS_NOT_HTTPS = 'PrefetchNotEligibleSchemeIsNotHttps'
    PREFETCH_NOT_ELIGIBLE_USER_HAS_COOKIES = 'PrefetchNotEligibleUserHasCookies'
    PREFETCH_NOT_ELIGIBLE_USER_HAS_SERVICE_WORKER = 'PrefetchNotEligibleUserHasServiceWorker'
    PREFETCH_NOT_ELIGIBLE_USER_HAS_SERVICE_WORKER_NO_FETCH_HANDLER = 'PrefetchNotEligibleUserHasServiceWorkerNoFetchHandler'
    PREFETCH_NOT_ELIGIBLE_REDIRECT_FROM_SERVICE_WORKER = 'PrefetchNotEligibleRedirectFromServiceWorker'
    PREFETCH_NOT_ELIGIBLE_REDIRECT_TO_SERVICE_WORKER = 'PrefetchNotEligibleRedirectToServiceWorker'
    PREFETCH_NOT_ELIGIBLE_BATTERY_SAVER_ENABLED = 'PrefetchNotEligibleBatterySaverEnabled'
    PREFETCH_NOT_ELIGIBLE_PRELOADING_DISABLED = 'PrefetchNotEligiblePreloadingDisabled'
    PREFETCH_NOT_FINISHED_IN_TIME = 'PrefetchNotFinishedInTime'
    PREFETCH_NOT_STARTED = 'PrefetchNotStarted'
    PREFETCH_NOT_USED_COOKIES_CHANGED = 'PrefetchNotUsedCookiesChanged'
    PREFETCH_PROXY_NOT_AVAILABLE = 'PrefetchProxyNotAvailable'
    PREFETCH_RESPONSE_USED = 'PrefetchResponseUsed'
    PREFETCH_SUCCESSFUL_BUT_NOT_USED = 'PrefetchSuccessfulButNotUsed'
    PREFETCH_NOT_USED_PROBE_FAILED = 'PrefetchNotUsedProbeFailed'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PrefetchStatus: ...

@dataclass
class PrerenderMismatchedHeaders:
    header_name: str
    initial_value: str | None = ...
    activation_value: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PrerenderMismatchedHeaders: ...

def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class RuleSetUpdated:
    rule_set: RuleSet
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RuleSetUpdated: ...

@dataclass
class RuleSetRemoved:
    id_: RuleSetId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RuleSetRemoved: ...

@dataclass
class PreloadEnabledStateUpdated:
    disabled_by_preference: bool
    disabled_by_data_saver: bool
    disabled_by_battery_saver: bool
    disabled_by_holdback_prefetch_speculation_rules: bool
    disabled_by_holdback_prerender_speculation_rules: bool
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PreloadEnabledStateUpdated: ...

@dataclass
class PrefetchStatusUpdated:
    key: PreloadingAttemptKey
    pipeline_id: PreloadPipelineId
    initiating_frame_id: page.FrameId
    prefetch_url: str
    status: PreloadingStatus
    prefetch_status: PrefetchStatus
    request_id: network.RequestId
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PrefetchStatusUpdated: ...

@dataclass
class PrerenderStatusUpdated:
    key: PreloadingAttemptKey
    pipeline_id: PreloadPipelineId
    status: PreloadingStatus
    prerender_status: PrerenderFinalStatus | None
    disallowed_mojo_interface: str | None
    mismatched_headers: list[PrerenderMismatchedHeaders] | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PrerenderStatusUpdated: ...

@dataclass
class PreloadingAttemptSourcesUpdated:
    loader_id: network.LoaderId
    preloading_attempt_sources: list[PreloadingAttemptSource]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PreloadingAttemptSourcesUpdated: ...
