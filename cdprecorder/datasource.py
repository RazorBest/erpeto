from __future__ import annotations
import inspect
import json
import re
import urllib

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Optional, Sequence, Union, TYPE_CHECKING

from .str_evaluator import randomness_score

from .action import LowercaseStr

if TYPE_CHECKING:
    from .action import HttpAction


class ActionNotFound(ValueError):
    pass


class ReprSource:
    def __repr__(self):
        params = inspect.signature(self.__init__).parameters
        args = []
        for name in params:
            if not hasattr(self, name):
                continue
            args.append(f"{name}={getattr(self, name)!r}")
        args_line = ", ".join(args)

        classname = self.__class__.__name__
        return f"{classname}({args_line})"


class DataSource(ABC, ReprSource):
    @abstractmethod
    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        pass


class GroupDataSource():
    def __init__(sources: list[DataSource]):
        self.sources = sources


class ActionDataSource(ABC):
    def __init__(self, index: int):
        self.__index = index

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        if self.__index >= len(prev_actions):
            raise ActionNotFound(self.__index)
        action = prev_actions[self.__index]
        if action is None:
            return None
        return self.get_value_from_action(action)

    @abstractmethod
    def get_value_from_action(self, action: HttpAction) -> Optional[str]:
        pass

    def __repr__(self):
        params = inspect.signature(self.__init__).parameters
        args = []
        for name in params:
            if name == "index":
                args.append(f"{name}={self.__index!r}")
                continue
            args.append(f"{name}={getattr(self, name)!r}")
        args_line = ", ".join(args)

        classname = self.__class__.__name__
        return f"{classname}({args_line})"


class IntermediaryDataSource:
    def __init__(self, upper_source: DataSource) -> None:
        self.upper_source = upper_source

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        upper_source_value = self.upper_source.get_value(prev_actions)
        return self.get_value_from_upper_value(upper_source_value)

    @abstractmethod
    def get_value_from_upper_value(self, upper_value: str) -> Optional[str]:
        pass


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

        try:
            data = src_data
            for key in self.path:
                data = data[key]
        except LookupError:
            return None


class JSONFieldTarget:
    def __init__(self, source: DataSource, path: list[Union[int, str]]):
        self.source = source
        self.path = path

    def apply(self, container_data: object, prev_actions: list[Optional[HttpAction]]) -> None:
        value = self.source.get_value(prev_actions)
        if value is None:
            return

        try:
            data = container_data
            for key in self.path[:-1]:
                data = data[key]

            if not isinstance(data, list) and not isinstance(data, dict):
                return

            if isinstance(data, dict) and self.path[-1] not in data:
                return

            data[self.path[-1]] = value
        except LookupError:
            return


class JSONContainer(DataSource):
    def __init__(self, schema: JSONSchema, targets: list[DataSource]):
        self.data = schema.data
        self.targets: list[JSONFieldTarget] = targets

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        data = deepcopy(self.data)

        for target in self.targets:
            target.apply(data, prev_actions)

        return json.dumps(data)
