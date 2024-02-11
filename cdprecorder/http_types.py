from __future__ import annotations
import urllib

from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import http

class Cookie:
    def __init__(self, name: str = "", value: str = "", expires: Optional[Union[str, int]] = None, path: Optional[str] = None, samesite: Optional[str] = None, httponly: Optional[str] = None):
        self.name = name
        self.value = value
        self.expires = expires
        self.path = path
        self.samesite = samesite
        self.httponly = httponly

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, value={self.value!r}, expires={self.expires!r}, path={self.path!r}, samesite={self.samesite!r})"

    def to_dict(self) -> dict[str, str]:
        return {self.name: self.value}

    @classmethod
    def list_from_cookiejar(cls, cookie_jar: http.cookiejar.CookieJar) -> list[Cookie]:
        cookies = []
        for cookie in cookie_jar:
            obj = cls(
                getattr(cookie, "name", ""),
                getattr(cookie, "value", ""),
                cookie.expires,
                cookie.path,
                None,
                None,
            )
            cookies.append(obj)

        return cookies


def parse_cookie(data: str) -> Cookie:
    found_name = False
    cookie = Cookie("", "")
    for token in data.split(";"):
        token = token.strip()
        key, val, *_ = token.split("=") + [""]
        if not found_name:
            found_name = True
            cookie = Cookie(key, urllib.parse.unquote(val))
            continue

        if key == "expires":
            cookie.expires = val
        elif key == "path":
            cookie.path = val
        elif key == "samesite":
            cookie.samesite = val
        elif key == "httponly":
            cookie.httponly = val

    return cookie
