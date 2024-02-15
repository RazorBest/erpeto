from __future__ import annotations
import inspect

from typing import TYPE_CHECKING

from . import action
from . import datasource
from . import datatarget

if TYPE_CHECKING:
    import types


IMPORTS = \
"""from __future__ import annotations
import re
import requests
import urllib

from requests import Session
from abc import ABC, abstractmethod


"""


REQUEST_ACTION_DEFINITION = \
"""class RequestAction:
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


"""


RESPONSE_ACTION_DEFINITION = \
"""class ResponseAction:
    def __init__(self, url=None, headers=None, body=None, cookies=None, status=None):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.body = body
        self.status = status


"""


COOKIE_DEFINITION = \
"""class Cookie:
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


"""

LOWERCASESTR_DEFINITION = \
"""class LowercaseStr(str):
    def __new__(cls, value: str, *args: object, **kwargs: object) -> LowercaseStr:
        return super(LowercaseStr, cls).__new__(cls, value.lower(), *args, **kwargs)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(str(other).lower())

    def __hash__(self) -> int:
        return super().__hash__()


"""


INTERMEDIARY_DATASOURCE_DEFINITION = \
"""class IntermediaryDataSource:
    def __init__(self, upper_source):
        self.upper_source = upper_source

    def get_value(self, prev_actions):
        upper_source_value = self.upper_source.get_value(prev_actions)
        return get_value_from_upper_value(self.upper_source)


"""


def get_module_level_classes(module: types.ModuleType) -> list[type]:
    module_name = module.__name__

    classes: list[type] = []
    for name, obj in inspect.getmembers(module):
        if not inspect.isclass(obj) or obj.__module__ != module_name:
            continue
        classes.append(obj)

    return classes

def generate_datasource_definitions() -> str:
    content = ""

    content += inspect.getsource(datasource.DataSource) + "\n\n"
    content += inspect.getsource(datasource.IntermediaryDataSource) + "\n\n"
    for obj in get_module_level_classes(datasource):
        if not issubclass(obj, datasource.DataSource):
            continue
        if obj == datasource.DataSource or obj == datasource.IntermediaryDataSource:
            continue

        content += inspect.getsource(obj) + "\n\n"

    return content


def generate_datatarget_definitions() -> str:
    content = ""
    for obj in get_module_level_classes(datatarget):
        content += inspect.getsource(obj) + "\n\n"

    return content


def generate_action_functions() -> str:
    return inspect.getsource(action.response_action_from_python_response) + "\n\n"


def generate_definitions() -> str:
    content = ""
    content += IMPORTS
    content += LOWERCASESTR_DEFINITION
    content += COOKIE_DEFINITION
    content += REQUEST_ACTION_DEFINITION
    content += RESPONSE_ACTION_DEFINITION
    content += INTERMEDIARY_DATASOURCE_DEFINITION
    content += generate_datasource_definitions()
    content += generate_datatarget_definitions()
    content += generate_action_functions()

    content = content.rstrip()

    return content
