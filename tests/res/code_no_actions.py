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


class DynamicRepr:

    def __repr__(self):
        params = inspect.signature(self.__init__).parameters
        args = []
        for name in params:
            if not hasattr(self, name):
                continue
            args.append(f'{name}={getattr(self, name)!r}')
        args_line = ', '.join(args)
        classname = self.__class__.__name__
        return f'{classname}({args_line})'

class DataSource(ABC, DynamicRepr):

    @abstractmethod
    def get_value(self, prev_actions):

class IntermediaryDataSource:

    def __init__(self, upper_source):
        self.upper_source = upper_source

    def get_value(self, prev_actions):
        upper_source_value = self.upper_source.get_value(prev_actions)
        if upper_source_value is None:
            return None
        return self.get_value_from_upper_value(upper_source_value)

    @abstractmethod
    def get_value_from_upper_value(self, upper_value):

class StrSource(DataSource):

    def __init__(self, text):
        self.text = text

    def get_value(self, prev_actions):
        return self.text

class JSONContainer(DataSource):

    def __init__(self, schema, targets):
        self.data = schema.data
        self.targets = targets

    def get_value(self, prev_actions):
        data = deepcopy(self.data)
        for target in self.targets:
            target.apply(data, prev_actions)
        return json.dumps(data)

class SingleSourcedTarget(ABC):

    def __init__(self, source):
        self.source = source

    def apply(self, action, prev_actions):
        value = self.source.get_value(prev_actions)
        if value is None:
            return
        self.apply_value(action, value)

    @abstractmethod
    def apply_value(self, action, value):
        pass

class CookieTarget(SingleSourcedTarget):

    def __init__(self, name, source):
        super().__init__(source)
        self.name = name

    def apply_value(self, action, value):
        for cookie in action.cookies:
            if cookie.name == self.name:
                cookie.value = value
                break
        else:
            action.cookies.append(Cookie(self.name, value))

class HeaderTarget(SingleSourcedTarget):

    def __init__(self, source, key, value):
        super().__init__(source)
        self.key = LowercaseStr(key)
        self.value = value

    def apply_value(self, action, value):
        action.headers[self.key] = value

class BodyTarget(SingleSourcedTarget):

    def apply_value(self, action, value):
        action.body = value.encode()

def response_action_from_python_response(resp):
    headers = {}
    for (key, val) in resp.headers.items():
        if key.startswith(':'):
            continue
        headers[LowercaseStr(key)] = val
    cookies = Cookie.list_from_cookiejar(resp.cookies)
    return ResponseAction(url=resp.url, headers=headers, cookies=cookies, body=resp.raw, status=resp.status_code)


actions = []
