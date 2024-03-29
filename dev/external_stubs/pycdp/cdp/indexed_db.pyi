import typing
from . import runtime as runtime, storage as storage
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

@dataclass
class DatabaseWithObjectStores:
    name: str
    version: float
    object_stores: typing.List[ObjectStore]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DatabaseWithObjectStores: ...
    def __init__(self, name, version, object_stores) -> None: ...

@dataclass
class ObjectStore:
    name: str
    key_path: KeyPath
    auto_increment: bool
    indexes: typing.List[ObjectStoreIndex]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ObjectStore: ...
    def __init__(self, name, key_path, auto_increment, indexes) -> None: ...

@dataclass
class ObjectStoreIndex:
    name: str
    key_path: KeyPath
    unique: bool
    multi_entry: bool
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ObjectStoreIndex: ...
    def __init__(self, name, key_path, unique, multi_entry) -> None: ...

@dataclass
class Key:
    type_: str
    number: typing.Optional[float] = ...
    string: typing.Optional[str] = ...
    date: typing.Optional[float] = ...
    array: typing.Optional[typing.List[Key]] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Key: ...
    def __init__(self, type_, number, string, date, array) -> None: ...

@dataclass
class KeyRange:
    lower_open: bool
    upper_open: bool
    lower: typing.Optional[Key] = ...
    upper: typing.Optional[Key] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> KeyRange: ...
    def __init__(self, lower_open, upper_open, lower, upper) -> None: ...

@dataclass
class DataEntry:
    key: runtime.RemoteObject
    primary_key: runtime.RemoteObject
    value: runtime.RemoteObject
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DataEntry: ...
    def __init__(self, key, primary_key, value) -> None: ...

@dataclass
class KeyPath:
    type_: str
    string: typing.Optional[str] = ...
    array: typing.Optional[typing.List[str]] = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> KeyPath: ...
    def __init__(self, type_, string, array) -> None: ...

def clear_object_store(database_name: str, object_store_name: str, security_origin: typing.Optional[str] = None, storage_key: typing.Optional[str] = None, storage_bucket: typing.Optional[storage.StorageBucket] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def delete_database(database_name: str, security_origin: typing.Optional[str] = None, storage_key: typing.Optional[str] = None, storage_bucket: typing.Optional[storage.StorageBucket] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def delete_object_store_entries(database_name: str, object_store_name: str, key_range: KeyRange, security_origin: typing.Optional[str] = None, storage_key: typing.Optional[str] = None, storage_bucket: typing.Optional[storage.StorageBucket] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def request_data(database_name: str, object_store_name: str, index_name: str, skip_count: int, page_size: int, security_origin: typing.Optional[str] = None, storage_key: typing.Optional[str] = None, storage_bucket: typing.Optional[storage.StorageBucket] = None, key_range: typing.Optional[KeyRange] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[typing.List[DataEntry], bool]]: ...
def get_metadata(database_name: str, object_store_name: str, security_origin: typing.Optional[str] = None, storage_key: typing.Optional[str] = None, storage_bucket: typing.Optional[storage.StorageBucket] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[float, float]]: ...
def request_database(database_name: str, security_origin: typing.Optional[str] = None, storage_key: typing.Optional[str] = None, storage_bucket: typing.Optional[storage.StorageBucket] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, DatabaseWithObjectStores]: ...
def request_database_names(security_origin: typing.Optional[str] = None, storage_key: typing.Optional[str] = None, storage_bucket: typing.Optional[storage.StorageBucket] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[str]]: ...
