import typing
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

@dataclass
class Domain:
    name: str
    version: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Domain: ...
    def __init__(self, name, version) -> None: ...

def get_domains() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[Domain]]: ...
