import typing
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class DatabaseId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> DatabaseId: ...

@dataclass
class Database:
    id_: DatabaseId
    domain: str
    name: str
    version: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Database: ...

@dataclass
class Error:
    message: str
    code: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Error: ...

def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def execute_sql(database_id: DatabaseId, query: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, tuple[list[str] | None, list[typing.Any] | None, Error | None]]: ...
def get_database_table_names(database_id: DatabaseId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, list[str]]: ...

@dataclass
class AddDatabase:
    database: Database
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AddDatabase: ...
