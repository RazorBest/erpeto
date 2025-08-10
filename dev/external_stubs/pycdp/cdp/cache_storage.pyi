import enum
import typing
from . import storage as storage
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class CacheId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CacheId: ...

class CachedResponseType(enum.Enum):
    BASIC = 'basic'
    CORS = 'cors'
    DEFAULT = 'default'
    ERROR = 'error'
    OPAQUE_RESPONSE = 'opaqueResponse'
    OPAQUE_REDIRECT = 'opaqueRedirect'
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> CachedResponseType: ...

@dataclass
class DataEntry:
    request_url: str
    request_method: str
    request_headers: list[Header]
    response_time: float
    response_status: int
    response_status_text: str
    response_type: CachedResponseType
    response_headers: list[Header]
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DataEntry: ...

@dataclass
class Cache:
    cache_id: CacheId
    security_origin: str
    storage_key: str
    cache_name: str
    storage_bucket: storage.StorageBucket | None = ...
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Cache: ...

@dataclass
class Header:
    name: str
    value: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Header: ...

@dataclass
class CachedResponse:
    body: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CachedResponse: ...

def delete_cache(cache_id: CacheId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def delete_entry(cache_id: CacheId, request: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def request_cache_names(security_origin: str | None = None, storage_key: str | None = None, storage_bucket: storage.StorageBucket | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[Cache]]: ...
def request_cached_response(cache_id: CacheId, request_url: str, request_headers: list[Header]) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, CachedResponse]: ...
def request_entries(cache_id: CacheId, skip_count: int | None = None, page_size: int | None = None, path_filter: str | None = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[list[DataEntry], float]]: ...
