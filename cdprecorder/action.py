from __future__ import annotations

#from typing import Optional

from .http_types import Cookie, parse_cookie


class LowercaseStr(str):
    def __new__(cls, value: str, *args: object, **kwargs: object) -> LowercaseStr:
        return super(LowercaseStr, cls).__new__(cls, value.lower(), *args, **kwargs)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(str(other).lower())

    def __hash__(self) -> int:
        return super().__hash__()


class BrowserAction:
    def __init__(self) -> None:
        self.targets: list[HttpTarget] = []


class InputAction(BrowserAction):
    def __init__(self, text: str, selector: str, timestamp: float) -> None:
        super().__init__()
        self.text = text
        self.selector = selector
        self.timestamp = timestamp


class HttpAction(BrowserAction):
    def __init__(self, request_data: Optional[RequestInfo] = None,
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
            cookie_key: Optional[str] = None
            for key, val in data.headers.items():
                if key.lower() == "cookie":
                    cookie_key = key
                    break

            if cookie_key:
                val = data.headers[cookie_key]
                self.cookies += [parse_cookie(block) for block in val.split(";")]
                del data.headers[cookie_key]

            for key, val in data.headers.items():
                # Ignore pseudo-headers: https://www.rfc-editor.org/rfc/rfc7540#section-8.1.2.1
                if key.startswith(":"):
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
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.has_response = False


class ResponseAction(HttpAction):
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
