import typing
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass as dataclass

def clear_device_orientation_override() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def set_device_orientation_override(alpha: float, beta: float, gamma: float) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
