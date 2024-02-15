from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

from .action import LowercaseStr
from cdprecorder.http_types import Cookie

if TYPE_CHECKING:
    from .action import HttpAction
    from .datasource import DataSource


class SingleSourcedTarget(ABC):
    def __init__(self, source: DataSource):
        self.source = source

    def apply(self, action: HttpAction, prev_actions: list[Optional[HttpAction]]) -> None:
        value = self.source.get_value(prev_actions)
        if value is None:
            return
        self.apply_value(action, value)

    @abstractmethod
    def apply_value(self, action: HttpAction, value: str) -> None:
        pass


class CookieTarget(SingleSourcedTarget):
    def __init__(self, name: str, source: DataSource):
        super().__init__(source)
        self.name = name

    def apply_value(self, action: HttpAction, value: str) -> None:
        for cookie in action.cookies:
            if cookie.name == self.name:
                cookie.value = value
                break
        else:
            action.cookies.append(Cookie(self.name, value))


class HeaderTarget(SingleSourcedTarget):
    def __init__(self, source: DataSource, key: str, value: str):
        super().__init__(source)
        self.key = LowercaseStr(key)
        self.value = value

    def apply_value(self, action: HttpAction, value: str) -> None:
        action.headers[self.key] = value


class BodyTarget(SingleSourcedTarget):
    def apply_value(self, action: HttpAction, value:str) -> None:
        action.body = value.encode()
