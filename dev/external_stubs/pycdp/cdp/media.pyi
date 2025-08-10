import typing
from .util import T_JSON_DICT as T_JSON_DICT, event_class as event_class
from dataclasses import dataclass

class PlayerId(str):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, json: str) -> PlayerId: ...

class Timestamp(float):
    def to_json(self) -> float: ...
    @classmethod
    def from_json(cls, json: float) -> Timestamp: ...

@dataclass
class PlayerMessage:
    level: str
    message: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PlayerMessage: ...

@dataclass
class PlayerProperty:
    name: str
    value: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PlayerProperty: ...

@dataclass
class PlayerEvent:
    timestamp: Timestamp
    value: str
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PlayerEvent: ...

@dataclass
class PlayerErrorSourceLocation:
    file: str
    line: int
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PlayerErrorSourceLocation: ...

@dataclass
class PlayerError:
    error_type: str
    code: int
    stack: list[PlayerErrorSourceLocation]
    cause: list[PlayerError]
    data: dict
    def to_json(self) -> T_JSON_DICT: ...
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PlayerError: ...

def enable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...
def disable() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, None]: ...

@dataclass
class PlayerPropertiesChanged:
    player_id: PlayerId
    properties: list[PlayerProperty]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PlayerPropertiesChanged: ...

@dataclass
class PlayerEventsAdded:
    player_id: PlayerId
    events: list[PlayerEvent]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PlayerEventsAdded: ...

@dataclass
class PlayerMessagesLogged:
    player_id: PlayerId
    messages: list[PlayerMessage]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PlayerMessagesLogged: ...

@dataclass
class PlayerErrorsRaised:
    player_id: PlayerId
    errors: list[PlayerError]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PlayerErrorsRaised: ...

@dataclass
class PlayersCreated:
    players: list[PlayerId]
    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PlayersCreated: ...
