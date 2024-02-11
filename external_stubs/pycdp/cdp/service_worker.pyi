import enum
import typing
from . import target as target
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class RegistrationID(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> RegistrationID: ...

@dataclass
class ServiceWorkerRegistration:
    registration_id: RegistrationID
    scope_url: str
    is_deleted: bool
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ServiceWorkerRegistration: ...
    def __init__(self, registration_id, scope_url, is_deleted) -> None: ...

class ServiceWorkerVersionRunningStatus(enum.Enum):
    STOPPED: str
    STARTING: str
    RUNNING: str
    STOPPING: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ServiceWorkerVersionRunningStatus: ...

class ServiceWorkerVersionStatus(enum.Enum):
    NEW: str
    INSTALLING: str
    INSTALLED: str
    ACTIVATING: str
    ACTIVATED: str
    REDUNDANT: str
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> ServiceWorkerVersionStatus: ...

@dataclass
class ServiceWorkerVersion:
    version_id: str
    registration_id: RegistrationID
    script_url: str
    running_status: ServiceWorkerVersionRunningStatus
    status: ServiceWorkerVersionStatus
    script_last_modified: typing.Optional[float] = ...
    script_response_time: typing.Optional[float] = ...
    controlled_clients: typing.Optional[typing.List[target.TargetID]] = ...
    target_id: typing.Optional[target.TargetID] = ...
    router_rules: typing.Optional[str] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ServiceWorkerVersion: ...
    def __init__(self, version_id, registration_id, script_url, running_status, status, script_last_modified, script_response_time, controlled_clients, target_id, router_rules) -> None: ...

@dataclass
class ServiceWorkerErrorMessage:
    error_message: str
    registration_id: RegistrationID
    version_id: str
    source_url: str
    line_number: int
    column_number: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ServiceWorkerErrorMessage: ...
    def __init__(self, error_message, registration_id, version_id, source_url, line_number, column_number) -> None: ...

def deliver_push_message(origin: str, registration_id: RegistrationID, data: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def dispatch_sync_event(origin: str, registration_id: RegistrationID, tag: str, last_chance: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def dispatch_periodic_sync_event(origin: str, registration_id: RegistrationID, tag: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def inspect_worker(version_id: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_force_update_on_page_load(force_update_on_page_load: bool) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def skip_waiting(scope_url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def start_worker(scope_url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def stop_all_workers() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def stop_worker(version_id: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def unregister(scope_url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def update_registration(scope_url: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class WorkerErrorReported:
    error_message: ServiceWorkerErrorMessage
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WorkerErrorReported: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, error_message) -> None: ...

@dataclass
class WorkerRegistrationUpdated:
    registrations: typing.List[ServiceWorkerRegistration]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WorkerRegistrationUpdated: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, registrations) -> None: ...

@dataclass
class WorkerVersionUpdated:
    versions: typing.List[ServiceWorkerVersion]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> WorkerVersionUpdated: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, versions) -> None: ...
