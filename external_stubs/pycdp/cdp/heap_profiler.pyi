import typing
from . import runtime as runtime
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class HeapSnapshotObjectId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> HeapSnapshotObjectId: ...

@dataclass
class SamplingHeapProfileNode:
    call_frame: runtime.CallFrame
    self_size: float
    id_: int
    children: typing.List[SamplingHeapProfileNode]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SamplingHeapProfileNode: ...
    def __init__(self, call_frame, self_size, id_, children) -> None: ...

@dataclass
class SamplingHeapProfileSample:
    size: float
    node_id: int
    ordinal: float
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SamplingHeapProfileSample: ...
    def __init__(self, size, node_id, ordinal) -> None: ...

@dataclass
class SamplingHeapProfile:
    head: SamplingHeapProfileNode
    samples: typing.List[SamplingHeapProfileSample]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> SamplingHeapProfile: ...
    def __init__(self, head, samples) -> None: ...

def add_inspected_heap_object(heap_object_id: HeapSnapshotObjectId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def collect_garbage() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def get_heap_object_id(object_id: runtime.RemoteObjectId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, HeapSnapshotObjectId]: ...
def get_object_by_heap_object_id(object_id: HeapSnapshotObjectId, object_group: typing.Optional[str] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, runtime.RemoteObject]: ...
def get_sampling_profile() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, SamplingHeapProfile]: ...
def start_sampling(sampling_interval: typing.Optional[float] = None, include_objects_collected_by_major_gc: typing.Optional[bool] = None, include_objects_collected_by_minor_gc: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def start_tracking_heap_objects(track_allocations: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def stop_sampling() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, SamplingHeapProfile]: ...
def stop_tracking_heap_objects(report_progress: typing.Optional[bool] = None, treat_global_objects_as_roots: typing.Optional[bool] = None, capture_numeric_value: typing.Optional[bool] = None, expose_internals: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def take_heap_snapshot(report_progress: typing.Optional[bool] = None, treat_global_objects_as_roots: typing.Optional[bool] = None, capture_numeric_value: typing.Optional[bool] = None, expose_internals: typing.Optional[bool] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class AddHeapSnapshotChunk:
    chunk: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AddHeapSnapshotChunk: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, chunk) -> None: ...

@dataclass
class HeapStatsUpdate:
    stats_update: typing.List[int]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> HeapStatsUpdate: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, stats_update) -> None: ...

@dataclass
class LastSeenObjectId:
    last_seen_object_id: int
    timestamp: float
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LastSeenObjectId: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, last_seen_object_id, timestamp) -> None: ...

@dataclass
class ReportHeapSnapshotProgress:
    done: int
    total: int
    finished: typing.Optional[bool]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ReportHeapSnapshotProgress: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, done, total, finished) -> None: ...

@dataclass
class ResetProfiles:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ResetProfiles: ...
    def to_json(self) -> T_JSON_DICT: ...
