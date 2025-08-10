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

@dataclass
class TargetCrashed:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TargetCrashed: ...

@dataclass
class TargetReloadedAfterCrash:
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TargetReloadedAfterCrash: ...
