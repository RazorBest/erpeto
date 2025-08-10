from __future__ import annotations

import ast
import inspect
from typing import TYPE_CHECKING

from . import action, datasource, datatarget, util

if TYPE_CHECKING:
    import types


IMPORTS = """from __future__ import annotations
import re
import requests
import urllib

from requests import Session
from abc import ABC, abstractmethod


"""


REQUEST_ACTION_DEFINITION = """class RequestAction:
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


RESPONSE_ACTION_DEFINITION = """class ResponseAction:
    def __init__(self, url=None, headers=None, body=None, cookies=None, status=None):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.body = body
        self.status = status


"""


COOKIE_DEFINITION = """class Cookie:
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

LOWERCASESTR_DEFINITION = """class LowercaseStr(str):
    def __new__(cls, value: str, *args: object, **kwargs: object) -> LowercaseStr:
        return super(LowercaseStr, cls).__new__(cls, value.lower(), *args, **kwargs)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(str(other).lower())

    def __hash__(self) -> int:
        return super().__hash__()


"""


def get_source_code(obj: object, annotations: bool = False, docstrings: bool = False) -> str:
    source = inspect.getsource(obj)
    if annotations and docstrings:
        return source

    ast_obj = ast.parse(source)

    # Remove annotations from the python code
    if not annotations:
        for node in ast.walk(ast_obj):
            if "annotation" in node._fields:
                node.annotation = []
            if "returns" in node._fields:
                node.returns = []

            if "body" not in node._fields:
                continue

            for idx, child in enumerate(node.body):
                if not isinstance(child, ast.AnnAssign):
                    continue
                if "value" not in child._fields:
                    continue
                new_node = ast.Assign([child.target], child.value)
                ast.copy_location(new_node, child)
                node.body[idx] = new_node

    # Remove docstrings from the python code
    if not docstrings:
        for node in ast.walk(ast_obj):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                continue

            if len(node.body) == 0:
                continue

            # Check if the first child is a string expression
            first_child = node.body[0]
            if not isinstance(first_child, ast.Expr):
                continue

            if not isinstance(first_child.value, ast.Constant) or not isinstance(first_child.value.value, str):
                continue

            # The spec says that end_lineno is optional
            # https://docs.python.org/3.11/library/ast.html#ast.AST
            # We might handle this case in the future
            if first_child.end_lineno is None:
                continue

            removed_lines_count = first_child.end_lineno - first_child.lineno + 1

            # Remove the first child, which is the docstring
            old_node = node.body.pop(0)

            # Don't let the body be empty, because parsing won't work
            if len(node.body) == 0:
                new_node = ast.Pass()
                ast.copy_location(new_node, old_node)
                node.body.append(new_node)

            for child in node.body:
                ast.increment_lineno(child, n=-removed_lines_count)
    
    source = ast.unparse(ast_obj)

    return source


def get_module_level_classes(module: types.ModuleType) -> list[type]:
    module_name = module.__name__

    classes: list[tuple[int, type]] = []
    for _, obj in inspect.getmembers(module):
        if not inspect.isclass(obj) or obj.__module__ != module_name:
            continue
        line_number = inspect.getsourcelines(obj)[1]
        classes.append((line_number, obj))
    classes.sort()

    return [obj for _, obj in classes]


def generate_datasource_definitions() -> str:
    content = ""

    content += get_source_code(datasource.DataSource) + "\n\n"
    content += get_source_code(datasource.IntermediaryDataSource) + "\n\n"
    for obj in get_module_level_classes(datasource):
        if obj in (datasource.DataSource, datasource.IntermediaryDataSource):
            continue

        content += get_source_code(obj) + "\n\n"

    return content


def generate_datatarget_definitions() -> str:
    content = ""
    for obj in get_module_level_classes(datatarget):
        content += get_source_code(obj) + "\n\n"

    return content


def generate_action_functions() -> str:
    return get_source_code(action.response_action_from_python_response) + "\n\n"


def generate_util_definitions() -> str:
    content = ""
    for obj in get_module_level_classes(util):
        content += get_source_code(obj) + "\n\n"

    return content


def generate_definitions() -> str:
    content = ""
    content += IMPORTS
    content += LOWERCASESTR_DEFINITION
    content += COOKIE_DEFINITION
    content += REQUEST_ACTION_DEFINITION
    content += RESPONSE_ACTION_DEFINITION
    content += generate_util_definitions()
    content += generate_datasource_definitions()
    content += generate_datatarget_definitions()
    content += generate_action_functions()

    content = content.rstrip()

    return content
