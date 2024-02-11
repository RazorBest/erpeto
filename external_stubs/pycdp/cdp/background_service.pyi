import enum
import typing
from . import network as network, service_worker as service_worker
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class ServiceName(enum.Enum):
    BACKGROUND_FETCH: str
    BACKGROUND_SYNC: str
    PUSH_MESSAGING: str
    NOTIFICATIONS: str
    PAYMENT_HANDLER: str
    PERIODIC_BACKGROUND_SYNC: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ServiceName: ...

@dataclass
class EventMetadata:
    key: str
    value: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> EventMetadata: ...
    def __init__(self, key, value) -> None: ...

@dataclass
class BackgroundServiceEvent:
    timestamp: network.TimeSinceEpoch
    origin: str
    service_worker_registration_id: service_worker.RegistrationID
    service: ServiceName
    event_name: str
    instance_id: str
    event_metadata: typing.List[EventMetadata]
    storage_key: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackgroundServiceEvent: ...
    def __init__(self, timestamp, origin, service_worker_registration_id, service, event_name, instance_id, event_metadata, storage_key) -> None: ...

def start_observing(service: ServiceName) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def stop_observing(service: ServiceName) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_recording(should_record: bool, service: ServiceName) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def clear_events(service: ServiceName) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class RecordingStateChanged:
    is_recording: bool
    service: ServiceName
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RecordingStateChanged: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, is_recording, service) -> None: ...

@dataclass
class BackgroundServiceEventReceived:
    background_service_event: BackgroundServiceEvent
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackgroundServiceEventReceived: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, background_service_event) -> None: ...
