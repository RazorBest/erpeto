from __future__ import annotations
import inspect
import json
import re
import urllib

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Optional, Sequence, Union, TYPE_CHECKING

from .action import LowercaseStr
from .str_evaluator import randomness_score
from .util import DynamicRepr

if TYPE_CHECKING:
    from .action import HttpAction
    from .json_analyser import JSONSchema


class ActionNotFound(ValueError):
    pass


class DataSource(ABC, DynamicRepr):
    @abstractmethod
    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        """Returns the value obtained from the actions, if available."""


class ActionDataSource(ABC, DynamicRepr):
    def __init__(self, index: int):
        self.index = index

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        if self.index >= len(prev_actions):
            raise ActionNotFound(self.index)
        action = prev_actions[self.index]
        if action is None:
            return None
        return self.get_value_from_action(action)

    @abstractmethod
    def get_value_from_action(self, action: HttpAction) -> Optional[str]:
        """Returns the value obtained from one action, if available."""


class IntermediaryDataSource:
    def __init__(self, upper_source: DataSource) -> None:
        self.upper_source = upper_source

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        upper_source_value = self.upper_source.get_value(prev_actions)
        if upper_source_value is None:
            return None
        return self.get_value_from_upper_value(upper_source_value)

    @abstractmethod
    def get_value_from_upper_value(self, upper_value: str) -> Optional[str]:
        """Returns the value obtained by processing the upper value."""


class SubstrSource(IntermediaryDataSource):
    def __init__(self, upper_source: DataSource, start: int, end: int) -> None:
        super().__init__(upper_source)
        self.start = start
        self.end = end

    def get_value_from_upper_value(self, upper_value: str) -> Optional[str]:
        return upper_value[self.start:self.end]


class StrSource(DataSource):
    def __init__(self, text: str) -> None:
        self.text = text

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        return self.text


class HeaderSource(ActionDataSource):
    def __init__(self, index: int, key: str):
        super().__init__(index)
        self.key = LowercaseStr(key)

    def get_value_from_action(self, action: HttpAction) -> Optional[str]:
        if self.key not in action.headers:
            return None
        return action.headers[self.key]


class CookieSource(ActionDataSource):
    def __init__(self, index: int, name: str, strcontext: str):
        super().__init__(index)
        self.name = name
        self.strcontext = strcontext

    def get_value_from_action(self, action: HttpAction) -> Optional[str]:
        for cookie in action.cookies:
            if cookie.name == self.name:
                matched = re.match(self.strcontext, cookie.value)
                if matched is None:
                    return None

                return urllib.parse.unquote(matched[0])

        return None


class BodySource(ActionDataSource):
    def get_value_from_action(self, action: HttpAction) -> Optional[str]:
        if action.body is None:
            return None

        return action.body.decode("utf8")


def get_object_at_json_path(data: object, path: list[Union[str, int]]) -> Optional[object]:
    try:
        for key in path:
            if isinstance(data, list):
                if not isinstance(key, int):
                    return None
                data = data[key]
            elif isinstance(data, dict):
                data = data[key]
            else:
                return None
        return data
    except LookupError:
        return None


class JSONFieldSource(IntermediaryDataSource):
    def __init__(self, upper_source: DataSource, path: list[Union[str, int]]):
        super().__init__(upper_source)
        self.path = path

    def get_value_from_upper_value(self, upper_value: str) -> Optional[str]:
        src_data = None
        try:
            src_data = json.loads(upper_value)
        except json.JSONDecodeError: 
            return None

        data = get_object_at_json_path(src_data, self.path)
        if data is None:
            return None
        if isinstance(data, list) or isinstance(data, dict) or isinstance(data, bool):
            return json.dumps(data)

        return str(data)


class JSONFieldTarget:
    def __init__(self, source: DataSource, path: list[Union[int, str]]):
        self.source = source
        self.path = path

    def apply(self, container_data: object, prev_actions: Sequence[Optional[HttpAction]]) -> None:
        value = self.source.get_value(prev_actions)
        if value is None or len(self.path) == 0:
            return

        data = get_object_at_json_path(container_data, self.path[:-1])
        if data is None:
            return

        key = self.path[-1]
        if isinstance(data, list) and isinstance(key, int) and key < len(data):
            data[key] = value
        elif isinstance(data, dict) and key in data:
            data[key] = value


class JSONContainer(DataSource):
    def __init__(self, schema: JSONSchema, targets: list[JSONFieldTarget]):
        self.data = schema.data
        self.targets: list[JSONFieldTarget] = targets

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        data = deepcopy(self.data)

        for target in self.targets:
            target.apply(data, prev_actions)

        return json.dumps(data)
