import pytest
import requests

from cdprecorder.http_types import Cookie, parse_cookie


class TestCookie:
    def test_to_dict(self):
        cookie = Cookie(
            name="session1",
            value="test23dsahj%3D",
            expires="19:05:05",
            path="test.com",
            samesite="lax",
            httponly="false",
        )
        assert cookie.to_dict() == {"session1": "test23dsahj%3D"}

    def test_list_from_cookie_jar(self):
        cookiejar = requests.cookies.cookiejar_from_dict({
            "cookie1": "value1",
            "cookie2_": "value2",
        })
        expected = [
            Cookie("cookie1", "value1", path="/"),
            Cookie("cookie2_", "value2", path="/"),
        ] 
        assert Cookie.list_from_cookiejar(cookiejar) == expected
        

def test_parse_cookie():
    set_cookie_str = "XSRF-TOKEN=test12378; expires=Tue, 13 Feb 2024" \
        " 13:25:32 GMT; Max-Age=7200; path=/; secure; samesite=lax"

    expected = Cookie(
        "XSRF-TOKEN",
        "test12378",
        expires="Tue, 13 Feb 2024 13:25:32 GMT",
        path="/",
        samesite="lax",
    )
    assert parse_cookie(set_cookie_str) == expected
    
