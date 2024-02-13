from __future__ import annotations
import inspect
import json

from abc import ABC, abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING

from .str_evaluator import randomness_score

from .action import LowercaseStr

if TYPE_CHECKING:
    from .action import HttpAction

class ActionNotFound(ValueError):
    pass


class ReprSource:
    def __repr__(self):
        params = inspect.signature(self.__init__).parameters
        args = [f"{name}={getattr(self, name)!r}" for name in params]
        args_line = ", ".join(args)

        classname = self.__class__.__name__
        return f"{classname}({args_line})"


class DataSource(ABC, ReprSource):
    @abstractmethod
    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        pass


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
    def get_value_from_action(self, action: Optional[HttpAction]) -> Optional[str]:
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


class JSONField:
    def __init__(self, value: str, path: list[Union[str, int]], source: Optional[DataSource] = None):
        """
        Args:
            path: The list of keys/indexes to use to arrive to a JSON element.
        """
        self.value = value
        self.path = path
        self.source = source

    def apply(self, src_data: dict, prev_actions: Sequence[Optional[HttpAction]]) -> None:
        if self.source is None:
            return

        value = self.source.get_value(prev_actions)
        if value is None:
            return
        data = src_data
        for key in self.path[:-1]:
            data = data[key]

        last_key = self.path[-1]
        data[last_key] = value


class JSONSource(DataSource):
    def __init__(self, data: str, token_classifier: Optional[Callable[[str], bool]] = None):
        self.data = json.loads(data)

        if token_classifier is not None:
            self.classifier = token_classifier
        else:
            self.classifier = lambda token: randomness_score(token) >= 50

        self.targets: list[JSONField] = []
        self.classify_tokens()

    def _classify(self, data: object, path: list[Union[str, int]]) -> list[JSONField]:
        targets = []
        if isinstance(data, dict):
            for key, val in data.items():
                targets += self._classify(val, path + [key])
        elif isinstance(data, list):
            for index, val in enumerate(data):
                targets += self._classify(val, path + [index])
        elif isinstance(data, str):
            if self.classifier(data):
                target = JSONField(data, path)
                targets.append(target)
        # TODO: decide for int, bool, bytes etc

        return targets

    def classify_tokens(self) -> None:
        self.targets = self._classify(self.data, [])

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> str:
        for field_target in self.targets:
            if not field_target.source:
                continue
            field_target.apply(self.data, prev_actions)

        return json.dumps(self.data)
