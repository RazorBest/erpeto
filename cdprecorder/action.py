"""
This module contains objects called `actions`, representing http requests and
user interactions.

Classes:
    - LowercaseStr
    - BrowserAction: Base class for all actions.
    - InputAction: A user keyboard interaction with an HTML element.
    - HttpAction: Base class for HTTP requests and responses.
    - RequestAction: Represents an HTTP request.
    - ResponseAction: Represents an HTTP response.

Functions:
    - response_actions_from_python_response: Converts a response to a
    ResponseAction.


"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from .http_types import Cookie, parse_cookie

if TYPE_CHECKING:
    import requests

    from .type_checking import HttpTarget, RequestInfo


class LowercaseStr(str):
    """Subclass of str whose value is always lowercase."""

    def __new__(cls, value: str, *args: object, **kwargs: object) -> LowercaseStr:
        return super(LowercaseStr, cls).__new__(cls, value.lower(), *args, **kwargs)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(str(other).lower())

    def __hash__(self) -> int:
        return super().__hash__()


class BrowserAction:
    """Base class for all actions performed in Chrome."""
    def __init__(self) -> None:
        self.ID: int = -1
        self.targets: list[HttpTarget] = []


class InputAction(BrowserAction):
    """Represents a user keyboard interaction with an HTML element."""

    def __init__(self, text: str, selector: str, timestamp: float) -> None:
        super().__init__()
        self.text = text
        # The CSS selector to the HTML element corresponding to the action
        self.selector = selector
        self.timestamp = timestamp


class HttpAction(BrowserAction):
    """Represents an HTTP request or response. Can parse info from cdp events
    and python's requests objects. Contains helper methods for the execution
    of actions."""

    def __init__(
        self,
        request_data: Optional[RequestInfo] = None,
        body: Optional[bytes] = None,
        method: Optional[str] = None,
        headers: Optional[dict[LowercaseStr, str]] = None,
        url: Optional[str] = None,
        cookies: Optional[list[Cookie]] = None,
        status: Optional[int] = None,
    ):
        super().__init__()
        self.method = method
        if headers is not None:
            self.headers = headers
        else:
            self.headers = {}
        self.url = url
        self.body = body
        if cookies is not None:
            self.cookies = cookies
        else:
            self.cookies = []
        self.status = status

        if request_data is not None:
            self.update_info(request_data)

    def update_info(self, data: RequestInfo) -> None:
        if getattr(data, "headers", None):
            for key, val in data.headers.items():
                # Ignore pseudo-headers: https://www.rfc-editor.org/rfc/rfc7540#section-8.1.2.1
                if key.startswith(":"):
                    continue
                if key.lower() == "cookie":
                    self.cookies += [parse_cookie(block) for block in val.split(";")]
                    continue

                self.headers[LowercaseStr(key)] = val

        if hasattr(data, "cookies") and isinstance(data.cookies, list):
            self.cookies += data.cookies

        if hasattr(data, "url") and data.url is not None:
            self.url = data.url
        if hasattr(data, "method") and data.method is not None:
            self.method = data.method
        if hasattr(data, "status") and data.status is not None:
            self.status = data.status
        if hasattr(data, "status_code") and data.status_code is not None:
            self.status = data.status_code

    def set_body(self, body: bytes) -> None:
        self.body = body

    def shallow_copy_from_action(self, action: HttpAction) -> None:
        self.method = action.method
        self.headers = action.headers
        self.url = action.url
        self.body = action.body
        self.cookies = action.cookies
        self.status = action.status

    def cookies_to_dict(self) -> dict[str, str]:
        cookie_dict = {}
        for cookie in self.cookies:
            try:
                cookie_dict.update(cookie.to_dict())
            except Exception as exc:
                raise exc

        return cookie_dict

    def merge(self, action: Optional[HttpAction]) -> None:
        if action is None:
            return
        self.update_info(action)
        if action.body is not None:
            self.body = action.body

    def __eq__(self, obj: object) -> bool:
        if type(self) != type(obj):
            return False
        for key, val in vars(self).items():
            if not hasattr(obj, key):
                return False
            if val != getattr(obj, key):
                return False

        return True

    def __repr__(self) -> str:
        text = f"{self.__class__.__name__}("
        text += ",".join([f"{key}={val!r:.200}" for key, val in vars(self).items()])
        text += ")"

        return text


class RequestAction(HttpAction):
    """Represents an HTTP request."""

    def __init__(self, *args: Any, **kwargs: Any):
        self.has_response = kwargs.pop("has_response", False)
        self.type_ = kwargs.pop("type_", None)
        super().__init__(*args, **kwargs)


class ResponseAction(HttpAction):
    """Represents an HTTP response."""

    pass


def response_action_from_python_response(resp: requests.Response) -> ResponseAction:
    """Converts a python response from the requests module to a ResponseAction."""
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
        body=resp.text.encode(),
        status=resp.status_code,
    )
