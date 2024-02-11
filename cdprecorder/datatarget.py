from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .action import HttpAction, LowercaseStr
    from .datasource import DataSource

class CookieTarget:
    def __init__(self, name: str, source: DataSource):
        self.source = source
        self.name = name

    def apply(self, action: HttpAction, prev_actions: list[Optional[HttpAction]]) -> None:
        value = self.source.get_value(prev_actions)
        if value is None:
            return
        for cookie in action.cookies:
            if cookie.name == self.name:
                cookie.value = value
                break
        else:
            action.cookies.append(Cookie(self.cookie.name, value))


class HeaderTarget:
    def __init__(self, source: DataSource, key: LowercaseStr, value: str):
        self.source = source
        self.key = key
        self.value = value

    def apply(self, action: HttpAction, prev_actions: Sequence[Optional[HttpAction]]) -> None:
        value = self.source.get_value(prev_actions)
        if value is None:
            return
        action.headers[self.key] = value


class BodyTarget:
    def __init__(self, source: DataSource):
        self.source = source

    def apply(self, action: HttpAction, prev_actions: Sequence[Optional[HttpAction]]) -> None:
        value = self.source.get_value(prev_actions)
        if value is None:
            return
        action.body = value.encode()
