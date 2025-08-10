import typing
from . import network as network, storage as storage
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

@dataclass
class File:
    name: str
    last_modified: network.TimeSinceEpoch
    size: float
    type_: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> File: ...

@dataclass
class Directory:
    name: str
    nested_directories: list[str]
    nested_files: list[File]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Directory: ...

@dataclass
class BucketFileSystemLocator:
    storage_key: storage.SerializedStorageKey
    path_components: list[str]
    bucket_name: str | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BucketFileSystemLocator: ...

def get_directory(bucket_file_system_locator: BucketFileSystemLocator) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, Directory]: ...
