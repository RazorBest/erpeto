import enum
import typing
from . import browser as browser, network as network, page as page, target as target
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class SerializedStorageKey(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SerializedStorageKey: ...

class StorageType(enum.Enum):
    COOKIES = 'cookies'
    FILE_SYSTEMS = 'file_systems'
    INDEXEDDB = 'indexeddb'
    LOCAL_STORAGE = 'local_storage'
    SHADER_CACHE = 'shader_cache'
    WEBSQL = 'websql'
    SERVICE_WORKERS = 'service_workers'
    CACHE_STORAGE = 'cache_storage'
    INTEREST_GROUPS = 'interest_groups'
    SHARED_STORAGE = 'shared_storage'
    STORAGE_BUCKETS = 'storage_buckets'
    ALL_ = 'all'
    OTHER = 'other'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> StorageType: ...

@dataclass
class UsageForType:
    storage_type: StorageType
    usage: float
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> UsageForType: ...

@dataclass
class TrustTokens:
    issuer_origin: str
    count: float
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TrustTokens: ...

class InterestGroupAuctionId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> InterestGroupAuctionId: ...

class InterestGroupAccessType(enum.Enum):
    JOIN = 'join'
    LEAVE = 'leave'
    UPDATE = 'update'
    LOADED = 'loaded'
    BID = 'bid'
    WIN = 'win'
    ADDITIONAL_BID = 'additionalBid'
    ADDITIONAL_BID_WIN = 'additionalBidWin'
    TOP_LEVEL_BID = 'topLevelBid'
    TOP_LEVEL_ADDITIONAL_BID = 'topLevelAdditionalBid'
    CLEAR = 'clear'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> InterestGroupAccessType: ...

class InterestGroupAuctionEventType(enum.Enum):
    STARTED = 'started'
    CONFIG_RESOLVED = 'configResolved'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> InterestGroupAuctionEventType: ...

class InterestGroupAuctionFetchType(enum.Enum):
    BIDDER_JS = 'bidderJs'
    BIDDER_WASM = 'bidderWasm'
    SELLER_JS = 'sellerJs'
    BIDDER_TRUSTED_SIGNALS = 'bidderTrustedSignals'
    SELLER_TRUSTED_SIGNALS = 'sellerTrustedSignals'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> InterestGroupAuctionFetchType: ...

class SharedStorageAccessScope(enum.Enum):
    WINDOW = 'window'
    SHARED_STORAGE_WORKLET = 'sharedStorageWorklet'
    PROTECTED_AUDIENCE_WORKLET = 'protectedAudienceWorklet'
    HEADER = 'header'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SharedStorageAccessScope: ...

class SharedStorageAccessMethod(enum.Enum):
    ADD_MODULE = 'addModule'
    CREATE_WORKLET = 'createWorklet'
    SELECT_URL = 'selectURL'
    RUN = 'run'
    BATCH_UPDATE = 'batchUpdate'
    SET_ = 'set'
    APPEND = 'append'
    DELETE = 'delete'
    CLEAR = 'clear'
    GET = 'get'
    KEYS = 'keys'
    VALUES = 'values'
    ENTRIES = 'entries'
    LENGTH = 'length'
    REMAINING_BUDGET = 'remainingBudget'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SharedStorageAccessMethod: ...

@dataclass
class SharedStorageEntry:
    key: str
    value: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SharedStorageEntry: ...

@dataclass
class SharedStorageMetadata:
    creation_time: network.TimeSinceEpoch
    length: int
    remaining_budget: float
    bytes_used: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SharedStorageMetadata: ...

@dataclass
class SharedStoragePrivateAggregationConfig:
    filtering_id_max_bytes: int
    aggregation_coordinator_origin: str | None = ...
    context_id: str | None = ...
    max_contributions: int | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SharedStoragePrivateAggregationConfig: ...

@dataclass
class SharedStorageReportingMetadata:
    event_type: str
    reporting_url: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SharedStorageReportingMetadata: ...

@dataclass
class SharedStorageUrlWithMetadata:
    url: str
    reporting_metadata: list[SharedStorageReportingMetadata]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SharedStorageUrlWithMetadata: ...

@dataclass
class SharedStorageAccessParams:
    script_source_url: str | None = ...
    data_origin: str | None = ...
    operation_name: str | None = ...
    operation_id: str | None = ...
    keep_alive: bool | None = ...
    private_aggregation_config: SharedStoragePrivateAggregationConfig | None = ...
    serialized_data: str | None = ...
    urls_with_metadata: list[SharedStorageUrlWithMetadata] | None = ...
    urn_uuid: str | None = ...
    key: str | None = ...
    value: str | None = ...
    ignore_if_present: bool | None = ...
    worklet_ordinal: int | None = ...
    worklet_target_id: target.TargetID | None = ...
    with_lock: str | None = ...
    batch_update_id: str | None = ...
    batch_size: int | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SharedStorageAccessParams: ...

class StorageBucketsDurability(enum.Enum):
    RELAXED = 'relaxed'
    STRICT = 'strict'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> StorageBucketsDurability: ...

@dataclass
class StorageBucket:
    storage_key: SerializedStorageKey
    name: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> StorageBucket: ...

@dataclass
class StorageBucketInfo:
    bucket: StorageBucket
    id_: str
    expiration: network.TimeSinceEpoch
    quota: float
    persistent: bool
    durability: StorageBucketsDurability
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> StorageBucketInfo: ...

class AttributionReportingSourceType(enum.Enum):
    NAVIGATION = 'navigation'
    EVENT = 'event'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AttributionReportingSourceType: ...

class UnsignedInt64AsBase10(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> UnsignedInt64AsBase10: ...

class UnsignedInt128AsBase16(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> UnsignedInt128AsBase16: ...

class SignedInt64AsBase10(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> SignedInt64AsBase10: ...

@dataclass
class AttributionReportingFilterDataEntry:
    key: str
    values: list[str]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingFilterDataEntry: ...

@dataclass
class AttributionReportingFilterConfig:
    filter_values: list[AttributionReportingFilterDataEntry]
    lookback_window: int | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingFilterConfig: ...

@dataclass
class AttributionReportingFilterPair:
    filters: list[AttributionReportingFilterConfig]
    not_filters: list[AttributionReportingFilterConfig]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingFilterPair: ...

@dataclass
class AttributionReportingAggregationKeysEntry:
    key: str
    value: UnsignedInt128AsBase16
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingAggregationKeysEntry: ...

@dataclass
class AttributionReportingEventReportWindows:
    start: int
    ends: list[int]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingEventReportWindows: ...

class AttributionReportingTriggerDataMatching(enum.Enum):
    EXACT = 'exact'
    MODULUS = 'modulus'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AttributionReportingTriggerDataMatching: ...

@dataclass
class AttributionReportingAggregatableDebugReportingData:
    key_piece: UnsignedInt128AsBase16
    value: float
    types: list[str]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingAggregatableDebugReportingData: ...

@dataclass
class AttributionReportingAggregatableDebugReportingConfig:
    key_piece: UnsignedInt128AsBase16
    debug_data: list[AttributionReportingAggregatableDebugReportingData]
    budget: float | None = ...
    aggregation_coordinator_origin: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingAggregatableDebugReportingConfig: ...

@dataclass
class AttributionScopesData:
    values: list[str]
    limit: float
    max_event_states: float
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionScopesData: ...

@dataclass
class AttributionReportingNamedBudgetDef:
    name: str
    budget: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingNamedBudgetDef: ...

@dataclass
class AttributionReportingSourceRegistration:
    time: network.TimeSinceEpoch
    expiry: int
    trigger_data: list[float]
    event_report_windows: AttributionReportingEventReportWindows
    aggregatable_report_window: int
    type_: AttributionReportingSourceType
    source_origin: str
    reporting_origin: str
    destination_sites: list[str]
    event_id: UnsignedInt64AsBase10
    priority: SignedInt64AsBase10
    filter_data: list[AttributionReportingFilterDataEntry]
    aggregation_keys: list[AttributionReportingAggregationKeysEntry]
    trigger_data_matching: AttributionReportingTriggerDataMatching
    destination_limit_priority: SignedInt64AsBase10
    aggregatable_debug_reporting_config: AttributionReportingAggregatableDebugReportingConfig
    max_event_level_reports: int
    named_budgets: list[AttributionReportingNamedBudgetDef]
    debug_reporting: bool
    event_level_epsilon: float
    debug_key: UnsignedInt64AsBase10 | None = ...
    scopes_data: AttributionScopesData | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingSourceRegistration: ...

class AttributionReportingSourceRegistrationResult(enum.Enum):
    SUCCESS = 'success'
    INTERNAL_ERROR = 'internalError'
    INSUFFICIENT_SOURCE_CAPACITY = 'insufficientSourceCapacity'
    INSUFFICIENT_UNIQUE_DESTINATION_CAPACITY = 'insufficientUniqueDestinationCapacity'
    EXCESSIVE_REPORTING_ORIGINS = 'excessiveReportingOrigins'
    PROHIBITED_BY_BROWSER_POLICY = 'prohibitedByBrowserPolicy'
    SUCCESS_NOISED = 'successNoised'
    DESTINATION_REPORTING_LIMIT_REACHED = 'destinationReportingLimitReached'
    DESTINATION_GLOBAL_LIMIT_REACHED = 'destinationGlobalLimitReached'
    DESTINATION_BOTH_LIMITS_REACHED = 'destinationBothLimitsReached'
    REPORTING_ORIGINS_PER_SITE_LIMIT_REACHED = 'reportingOriginsPerSiteLimitReached'
    EXCEEDS_MAX_CHANNEL_CAPACITY = 'exceedsMaxChannelCapacity'
    EXCEEDS_MAX_SCOPES_CHANNEL_CAPACITY = 'exceedsMaxScopesChannelCapacity'
    EXCEEDS_MAX_TRIGGER_STATE_CARDINALITY = 'exceedsMaxTriggerStateCardinality'
    EXCEEDS_MAX_EVENT_STATES_LIMIT = 'exceedsMaxEventStatesLimit'
    DESTINATION_PER_DAY_REPORTING_LIMIT_REACHED = 'destinationPerDayReportingLimitReached'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AttributionReportingSourceRegistrationResult: ...

class AttributionReportingSourceRegistrationTimeConfig(enum.Enum):
    INCLUDE = 'include'
    EXCLUDE = 'exclude'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AttributionReportingSourceRegistrationTimeConfig: ...

@dataclass
class AttributionReportingAggregatableValueDictEntry:
    key: str
    value: float
    filtering_id: UnsignedInt64AsBase10
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingAggregatableValueDictEntry: ...

@dataclass
class AttributionReportingAggregatableValueEntry:
    values: list[AttributionReportingAggregatableValueDictEntry]
    filters: AttributionReportingFilterPair
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingAggregatableValueEntry: ...

@dataclass
class AttributionReportingEventTriggerData:
    data: UnsignedInt64AsBase10
    priority: SignedInt64AsBase10
    filters: AttributionReportingFilterPair
    dedup_key: UnsignedInt64AsBase10 | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingEventTriggerData: ...

@dataclass
class AttributionReportingAggregatableTriggerData:
    key_piece: UnsignedInt128AsBase16
    source_keys: list[str]
    filters: AttributionReportingFilterPair
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingAggregatableTriggerData: ...

@dataclass
class AttributionReportingAggregatableDedupKey:
    filters: AttributionReportingFilterPair
    dedup_key: UnsignedInt64AsBase10 | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingAggregatableDedupKey: ...

@dataclass
class AttributionReportingNamedBudgetCandidate:
    filters: AttributionReportingFilterPair
    name: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingNamedBudgetCandidate: ...

@dataclass
class AttributionReportingTriggerRegistration:
    filters: AttributionReportingFilterPair
    aggregatable_dedup_keys: list[AttributionReportingAggregatableDedupKey]
    event_trigger_data: list[AttributionReportingEventTriggerData]
    aggregatable_trigger_data: list[AttributionReportingAggregatableTriggerData]
    aggregatable_values: list[AttributionReportingAggregatableValueEntry]
    aggregatable_filtering_id_max_bytes: int
    debug_reporting: bool
    source_registration_time_config: AttributionReportingSourceRegistrationTimeConfig
    aggregatable_debug_reporting_config: AttributionReportingAggregatableDebugReportingConfig
    scopes: list[str]
    named_budgets: list[AttributionReportingNamedBudgetCandidate]
    debug_key: UnsignedInt64AsBase10 | None = ...
    aggregation_coordinator_origin: str | None = ...
    trigger_context_id: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingTriggerRegistration: ...

class AttributionReportingEventLevelResult(enum.Enum):
    SUCCESS = 'success'
    SUCCESS_DROPPED_LOWER_PRIORITY = 'successDroppedLowerPriority'
    INTERNAL_ERROR = 'internalError'
    NO_CAPACITY_FOR_ATTRIBUTION_DESTINATION = 'noCapacityForAttributionDestination'
    NO_MATCHING_SOURCES = 'noMatchingSources'
    DEDUPLICATED = 'deduplicated'
    EXCESSIVE_ATTRIBUTIONS = 'excessiveAttributions'
    PRIORITY_TOO_LOW = 'priorityTooLow'
    NEVER_ATTRIBUTED_SOURCE = 'neverAttributedSource'
    EXCESSIVE_REPORTING_ORIGINS = 'excessiveReportingOrigins'
    NO_MATCHING_SOURCE_FILTER_DATA = 'noMatchingSourceFilterData'
    PROHIBITED_BY_BROWSER_POLICY = 'prohibitedByBrowserPolicy'
    NO_MATCHING_CONFIGURATIONS = 'noMatchingConfigurations'
    EXCESSIVE_REPORTS = 'excessiveReports'
    FALSELY_ATTRIBUTED_SOURCE = 'falselyAttributedSource'
    REPORT_WINDOW_PASSED = 'reportWindowPassed'
    NOT_REGISTERED = 'notRegistered'
    REPORT_WINDOW_NOT_STARTED = 'reportWindowNotStarted'
    NO_MATCHING_TRIGGER_DATA = 'noMatchingTriggerData'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AttributionReportingEventLevelResult: ...

class AttributionReportingAggregatableResult(enum.Enum):
    SUCCESS = 'success'
    INTERNAL_ERROR = 'internalError'
    NO_CAPACITY_FOR_ATTRIBUTION_DESTINATION = 'noCapacityForAttributionDestination'
    NO_MATCHING_SOURCES = 'noMatchingSources'
    EXCESSIVE_ATTRIBUTIONS = 'excessiveAttributions'
    EXCESSIVE_REPORTING_ORIGINS = 'excessiveReportingOrigins'
    NO_HISTOGRAMS = 'noHistograms'
    INSUFFICIENT_BUDGET = 'insufficientBudget'
    INSUFFICIENT_NAMED_BUDGET = 'insufficientNamedBudget'
    NO_MATCHING_SOURCE_FILTER_DATA = 'noMatchingSourceFilterData'
    NOT_REGISTERED = 'notRegistered'
    PROHIBITED_BY_BROWSER_POLICY = 'prohibitedByBrowserPolicy'
    DEDUPLICATED = 'deduplicated'
    REPORT_WINDOW_PASSED = 'reportWindowPassed'
    EXCESSIVE_REPORTS = 'excessiveReports'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AttributionReportingAggregatableResult: ...

class AttributionReportingReportResult(enum.Enum):
    SENT = 'sent'
    PROHIBITED = 'prohibited'
    FAILED_TO_ASSEMBLE = 'failedToAssemble'
    EXPIRED = 'expired'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> AttributionReportingReportResult: ...

@dataclass
class RelatedWebsiteSet:
    primary_sites: list[str]
    associated_sites: list[str]
    service_sites: list[str]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RelatedWebsiteSet: ...

def get_storage_key_for_frame(frame_id: page.FrameId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, SerializedStorageKey]: ...
def clear_data_for_origin(origin: str, storage_types: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_data_for_storage_key(storage_key: str, storage_types: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_cookies(browser_context_id: browser.BrowserContextID | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[network.Cookie]]: ...
def set_cookies(cookies: list[network.CookieParam], browser_context_id: browser.BrowserContextID | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_cookies(browser_context_id: browser.BrowserContextID | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_usage_and_quota(origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[float, float, bool, list[UsageForType]]]: ...
def override_quota_for_origin(origin: str, quota_size: float | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def track_cache_storage_for_origin(origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def track_cache_storage_for_storage_key(storage_key: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def track_indexed_db_for_origin(origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def track_indexed_db_for_storage_key(storage_key: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def untrack_cache_storage_for_origin(origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def untrack_cache_storage_for_storage_key(storage_key: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def untrack_indexed_db_for_origin(origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def untrack_indexed_db_for_storage_key(storage_key: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_trust_tokens() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[TrustTokens]]: ...
def clear_trust_tokens(issuer_origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, bool]: ...
def get_interest_group_details(owner_origin: str, name: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, dict]: ...
def set_interest_group_tracking(enable: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_interest_group_auction_tracking(enable: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_shared_storage_metadata(owner_origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, SharedStorageMetadata]: ...
def get_shared_storage_entries(owner_origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[SharedStorageEntry]]: ...
def set_shared_storage_entry(owner_origin: str, key: str, value: str, ignore_if_present: bool | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def delete_shared_storage_entry(owner_origin: str, key: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_shared_storage_entries(owner_origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def reset_shared_storage_budget(owner_origin: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_shared_storage_tracking(enable: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_storage_bucket_tracking(storage_key: str, enable: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def delete_storage_bucket(bucket: StorageBucket) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def run_bounce_tracking_mitigations() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[str]]: ...
def set_attribution_reporting_local_testing_mode(enabled: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_attribution_reporting_tracking(enable: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def send_pending_attribution_reports() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, int]: ...
def get_related_website_sets() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[RelatedWebsiteSet]]: ...
def get_affected_urls_for_third_party_cookie_metadata(first_party_url: str, third_party_urls: list[str]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[str]]: ...
def set_protected_audience_k_anonymity(owner: str, name: str, hashes: list[str]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class CacheStorageContentUpdated:
    origin: str
    storage_key: str
    bucket_id: str
    cache_name: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CacheStorageContentUpdated: ...

@dataclass
class CacheStorageListUpdated:
    origin: str
    storage_key: str
    bucket_id: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CacheStorageListUpdated: ...

@dataclass
class IndexedDBContentUpdated:
    origin: str
    storage_key: str
    bucket_id: str
    database_name: str
    object_store_name: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> IndexedDBContentUpdated: ...

@dataclass
class IndexedDBListUpdated:
    origin: str
    storage_key: str
    bucket_id: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> IndexedDBListUpdated: ...

@dataclass
class InterestGroupAccessed:
    access_time: network.TimeSinceEpoch
    type_: InterestGroupAccessType
    owner_origin: str
    name: str
    component_seller_origin: str | None
    bid: float | None
    bid_currency: str | None
    unique_auction_id: InterestGroupAuctionId | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InterestGroupAccessed: ...

@dataclass
class InterestGroupAuctionEventOccurred:
    event_time: network.TimeSinceEpoch
    type_: InterestGroupAuctionEventType
    unique_auction_id: InterestGroupAuctionId
    parent_auction_id: InterestGroupAuctionId | None
    auction_config: dict | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InterestGroupAuctionEventOccurred: ...

@dataclass
class InterestGroupAuctionNetworkRequestCreated:
    type_: InterestGroupAuctionFetchType
    request_id: network.RequestId
    auctions: list[InterestGroupAuctionId]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> InterestGroupAuctionNetworkRequestCreated: ...

@dataclass
class SharedStorageAccessed:
    access_time: network.TimeSinceEpoch
    scope: SharedStorageAccessScope
    method: SharedStorageAccessMethod
    main_frame_id: page.FrameId
    owner_origin: str
    owner_site: str
    params: SharedStorageAccessParams
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SharedStorageAccessed: ...

@dataclass
class SharedStorageWorkletOperationExecutionFinished:
    finished_time: network.TimeSinceEpoch
    execution_time: int
    method: SharedStorageAccessMethod
    operation_id: str
    worklet_target_id: target.TargetID
    main_frame_id: page.FrameId
    owner_origin: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SharedStorageWorkletOperationExecutionFinished: ...

@dataclass
class StorageBucketCreatedOrUpdated:
    bucket_info: StorageBucketInfo
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> StorageBucketCreatedOrUpdated: ...

@dataclass
class StorageBucketDeleted:
    bucket_id: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> StorageBucketDeleted: ...

@dataclass
class AttributionReportingSourceRegistered:
    registration: AttributionReportingSourceRegistration
    result: AttributionReportingSourceRegistrationResult
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingSourceRegistered: ...

@dataclass
class AttributionReportingTriggerRegistered:
    registration: AttributionReportingTriggerRegistration
    event_level: AttributionReportingEventLevelResult
    aggregatable: AttributionReportingAggregatableResult
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingTriggerRegistered: ...

@dataclass
class AttributionReportingReportSent:
    url: str
    body: dict
    result: AttributionReportingReportResult
    net_error: int | None
    net_error_name: str | None
    http_status_code: int | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingReportSent: ...

@dataclass
class AttributionReportingVerboseDebugReportSent:
    url: str
    body: list[dict] | None
    net_error: int | None
    net_error_name: str | None
    http_status_code: int | None
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttributionReportingVerboseDebugReportSent: ...
