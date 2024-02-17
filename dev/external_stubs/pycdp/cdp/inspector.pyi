import typing
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class Detached:
    reason: str
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Detached: ...
    def to_json(self) -> T_JSON_DICT: ...
    def __init__(self, reason) -> None: ...

@dataclass
class TargetCrashed:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TargetCrashed: ...
    def to_json(self) -> T_JSON_DICT: ...

@dataclass
class TargetReloadedAfterCrash:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TargetReloadedAfterCrash: ...
    def to_json(self) -> T_JSON_DICT: ...