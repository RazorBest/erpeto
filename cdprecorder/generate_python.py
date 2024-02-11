from __future__ import annotations
import inspect

from typing import TYPE_CHECKING

from .action import RequestAction, ResponseAction, HttpAction
from .generate_definitions import generate_definitions

if TYPE_CHECKING:
    from .httponly import Cookies

REQUEST_ACTION_CONSTRUCTION_TEMPLATE = \
"""action_{request_index} = RequestAction(
    method={method!r},
    url={url!r},
    headers={headers},
    cookies={cookies},
    body={request_body_var},
    has_response={has_response!r},
)"""

REQUEST_SENDING_TEMPLATE = \
"""prepared_request_{request_index} = requests.Request(
    method={method!r},
    url={url!r},
    headers={action_var}.headers,
    data={action_var}.body,
    cookies={action_var}.cookies_to_dict(),
).prepare()
response_{request_index} = Session().send(prepared_request_{request_index}, allow_redirects=False)
actions.append(response_action_from_python_response(response_{request_index}))"""


def indent_lines(lines: str, spaces: int = 4):
    indent = " " * spaces
    return indent + f"\n{indent}".join(lines.split('\n'))


def generate_python_target(target):
    params = inspect.signature(target.__init__).parameters
    args = [f"{name}={getattr(target, name)!r}" for name in params]
    args_line = ", ".join(args)

    classname = target.__class__.__name__
    return f"{classname}({args_line})"


def generate_python_headers(headers: dict):
    elements = [f"    {key!r}: {val!r},\n" for key, val in headers.items()]
    content = "".join(elements)

    if not content:
        return "{}"

    return f"{{\n{content}}}"


def generate_python_cookies(cookies: list[Cookie]):
    content = ""
    for cookie in cookies:
        content += f"    Cookie({cookie.name!r}, {cookie.value!r}),\n"

    if not content:
        return "[]"

    return f"[\n{content}]"
    

def generate_python_request_action(request_index: int, action: RequestAction):
    body_var = "None"
    if action.body is not None:
        body_var = f"REQUEST_BODY_{request_index}"

    return REQUEST_ACTION_CONSTRUCTION_TEMPLATE.format(
        request_index=request_index, 
        method=action.method,
        url=action.url,
        headers=indent_lines(generate_python_headers(action.headers)).lstrip(),
        cookies=indent_lines(generate_python_cookies(action.cookies)).lstrip(),
        request_body_var=body_var,
        has_response=action.has_response,
    )


def generate_python_request(request_index: int, action: RequestAction):
    action_var = f"action_{request_index}"

    return REQUEST_SENDING_TEMPLATE.format(
        request_index=request_index,
        method=action.method,
        url=action.url,
        action_var=action_var,
    )


def generate_request_bodies(actions: list[HttpAction]):
    content = ""
    for index, action in enumerate(actions):
        if isinstance(action, RequestAction) and action.body is not None:
            content += f"REQUEST_BODY_{index} = {action.body!r}\n"

    content += "\n\n"

    return content


def generate_python_actions(actions: list[HttpAction]) -> None:
    lines = "actions = []\n\n"
    for index, action in enumerate(actions):
        if isinstance(action, RequestAction):
            action_construction = generate_python_request_action(index, action)
            lines += action_construction + "\n"
            lines += f"actions.append(action_{index})\n"
            for target in action.targets:
                target_str = generate_python_target(target)
                apply_call = f"{target_str}.apply(action_{index}, actions)"
                lines += apply_call + "\n"

            request_section = generate_python_request(index, action)
            lines += request_section + "\n\n"
        elif not isinstance(action, ResponseAction):
            lines += "actions.append(None)\n"

    return lines


def write_python_code(actions: list[HttpAction], path):
    code = ""
    code += generate_definitions()
    code += generate_request_bodies(actions)
    code += generate_python_actions(actions)

    with open(path, "w") as f:
        f.write(code)
