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
    def __init__(self, id_, domain, name, version) -> None: ...

@dataclass
class Error:
    message: str
    code: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Error: ...
    def __init__(self, message, code) -> None: ...

def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def execute_sql(database_id: DatabaseId, query: str) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[typing.Optional[typing.List[str]], typing.Optional[typing.List[typing.Any]], typing.Optional[Error]]]: ...
def get_database_table_names(database_id: DatabaseId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[str]]: ...

@dataclass
class AddDatabase:
    database: Database
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AddDatabase: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, database) -> None: ...
