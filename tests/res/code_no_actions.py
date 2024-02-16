from __future__ import annotations
import re
import requests
import urllib

from requests import Session
from abc import ABC, abstractmethod


class LowercaseStr(str):
    def __new__(cls, value: str, *args: object, **kwargs: object) -> LowercaseStr:
        return super(LowercaseStr, cls).__new__(cls, value.lower(), *args, **kwargs)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(str(other).lower())

    def __hash__(self) -> int:
        return super().__hash__()


class Cookie:
    def __init__(self, name = "", value = ""):
        self.name = name
        self.value = value

    def to_dict(self):
        return {self.name: self.value}

    @classmethod
    def list_from_cookiejar(cls, cookie_jar):
        cookies = []
        for cookie in cookie_jar:
            obj = cls(
                getattr(cookie, "name", ""),
                getattr(cookie, "value", ""),
            )
            cookies.append(obj)

        return cookies


class RequestAction:
    def __init__(self, method=None, url=None, headers=None, body=None, cookies=None, has_response=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.body = body
        self.has_response = has_response

    def cookies_to_dict(self) -> dict[str, str]:
        cookie_dict = {}
        for cookie in self.cookies:
            cookie_dict.update(cookie.to_dict())

        return cookie_dict


class ResponseAction:
    def __init__(self, url=None, headers=None, body=None, cookies=None, status=None):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.body = body
        self.status = status


class IntermediaryDataSource:
    def __init__(self, upper_source):
        self.upper_source = upper_source

    def get_value(self, prev_actions):
        upper_source_value = self.upper_source.get_value(prev_actions)
        return get_value_from_upper_value(self.upper_source)


class DataSource(ABC, DynamicRepr):
    @abstractmethod
    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        """Returns the value obtained from the actions, if available."""


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


class JSONContainer(DataSource):
    def __init__(self, schema: JSONSchema, targets: list[JSONFieldTarget]):
        self.data = schema.data
        self.targets: list[JSONFieldTarget] = targets

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        data = deepcopy(self.data)

        for target in self.targets:
            target.apply(data, prev_actions)

        return json.dumps(data)


class StrSource(DataSource):
    def __init__(self, text: str) -> None:
        self.text = text

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        return self.text


class BodyTarget(SingleSourcedTarget):
    def apply_value(self, action: HttpAction, value:str) -> None:
        action.body = value.encode()


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


def response_action_from_python_response(resp: requests.Response) -> ResponseAction:
    headers: dict[LowercaseStr, str] = {}
    for key, val in resp.headers.items():
        # Ignore pseudo-headers: https://www.rfc-editor.org/rfc/rfc7540#section-8.1.2.1
        if key.startswith(":"):
            continue
        headers[LowercaseStr(key)] = val

    cookies = Cookie.list_from_cookiejar(resp.cookies)
    return ResponseAction(
        url=resp.url,
        headers=headers,
        cookies=cookies,
        body=resp.raw,
        status=resp.status_code,
    )


actions = []
