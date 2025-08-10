import enum
import typing
from . import network as network, service_worker as service_worker
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class ServiceName(enum.Enum):
    BACKGROUND_FETCH = 'backgroundFetch'
    BACKGROUND_SYNC = 'backgroundSync'
    PUSH_MESSAGING = 'pushMessaging'
    NOTIFICATIONS = 'notifications'
    PAYMENT_HANDLER = 'paymentHandler'
    PERIODIC_BACKGROUND_SYNC = 'periodicBackgroundSync'
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

@dataclass
class BackgroundServiceEvent:
    timestamp: network.TimeSinceEpoch
    origin: str
    service_worker_registration_id: service_worker.RegistrationID
    service: ServiceName
    event_name: str
    instance_id: str
    event_metadata: list[EventMetadata]
    storage_key: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackgroundServiceEvent: ...

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

@dataclass
class BackgroundServiceEventReceived:
    background_service_event: BackgroundServiceEvent
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BackgroundServiceEventReceived: ...
