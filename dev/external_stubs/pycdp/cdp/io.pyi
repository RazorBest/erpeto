import typing
from . import runtime as runtime
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass as dataclass

class StreamHandle(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> StreamHandle: ...

def close(handle: StreamHandle) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def read(handle: StreamHandle, offset: typing.Optional[int] = None, size: typing.Optional[int] = None) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[typing.Optional[bool], str, bool]]: ...
def resolve_blob(object_id: runtime.RemoteObjectId) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, str]: ...