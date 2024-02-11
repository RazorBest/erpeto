import typing
from _typeshed import Incomplete

T_JSON_DICT = typing.Dict[str, typing.Any]
_event_parsers: dict

def event_class(method): ...
def parse_json_event(json: T_JSON_DICT) -> typing.Any: ...
