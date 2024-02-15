from __future__ import annotations
import pytest

from typing import TYPE_CHECKING

from .conftest import DummyDataSource

from cdprecorder.action import HttpAction, LowercaseStr
from cdprecorder.http_types import Cookie
from cdprecorder.datatarget import BodyTarget, CookieTarget, HeaderTarget


@pytest.fixture
def actions_list():
    action1 = HttpAction(
        headers={LowercaseStr("c"): "3"},
        cookies=[Cookie("a", "1")],
    )

    return [action1, None]


class TestCookieTarget:
    def test_apply(self, actions_list):
        source1 = DummyDataSource("v1")
        source2 = DummyDataSource("v2")
        source3 = DummyDataSource("v3")
        source4 = DummyDataSource(None)
        action = HttpAction()

        # Test new cookie insertion
        assert len(action.cookies) == 0
        CookieTarget("a", source1).apply(action, actions_list)
        assert len(action.cookies) == 1
        assert action.cookies[0].name == "a"
        assert action.cookies[0].value == "v1"

        # Test new cookie insertion, with other cookie present
        CookieTarget("B", source2).apply(action, actions_list)
        assert len(action.cookies) == 2
        assert action.cookies[1].name == "B"
        assert action.cookies[1].value == "v2"

        # Test existing cookie, changing value
        CookieTarget("B", source3).apply(action, actions_list)
        assert len(action.cookies) == 2
        assert action.cookies[1].name == "B"
        assert action.cookies[1].value == "v3"

        # Test cookie lowercase, being treated differently
        CookieTarget("b", source1).apply(action, actions_list)
        assert len(action.cookies) == 3
        assert action.cookies[2].name == "b"
        assert action.cookies[2].value == "v1"

        # Test with a data source that returns a None value
        CookieTarget("c", source4).apply(action, actions_list)
        assert len(action.cookies) == 3

        assert action.cookies[0].name == "a"
        assert action.cookies[1].name == "B"
        assert action.cookies[2].name == "b"

        assert action.url is None
        assert action.method is None
        assert action.body is None
        assert action.headers == dict()


class TestHeaderTarget:
    def test_apply(self, actions_list):
        source1 = DummyDataSource("v1")
        source2 = DummyDataSource("v2")
        source3 = DummyDataSource("v3")
        source4 = DummyDataSource(None)
        action = HttpAction()

        # Test new header insertion
        assert len(action.headers) == 0
        HeaderTarget(source1, "a", "default").apply(action, actions_list)
        assert len(action.headers) == 1
        assert "a" in action.headers
        assert action.headers["a"] == "v1"

        # Test new header insertion, with other header present
        HeaderTarget(source2, "B", "default").apply(action, actions_list)
        assert len(action.headers) == 2
        assert "B" not in action.headers
        assert "b" in action.headers
        assert action.headers["b"] == "v2"

        # Test existing header, changing value
        HeaderTarget(source3, "B", "default").apply(action, actions_list)
        assert len(action.headers) == 2
        assert "b" in action.headers
        assert action.headers["b"] == "v3"

        # Test header lowercase, to be treated the same as uppercase
        HeaderTarget(source1, "b", "default").apply(action, actions_list)
        assert len(action.headers) == 2
        assert "b" in action.headers
        assert action.headers["b"] == "v1"

        # Test with a data source that returns a None value
        HeaderTarget(source4, "c", "default").apply(action, actions_list)
        assert len(action.headers) == 2

        assert action.headers == {"a": "v1", "b": "v1"}

        assert action.url is None
        assert action.method is None
        assert action.body is None
        assert action.cookies == []


class TestBodyTarget:
    def test_apply(self, actions_list):
        source1 = DummyDataSource("v1")
        source2 = DummyDataSource("v2")
        source4 = DummyDataSource(None)
        action = HttpAction()

        assert action.body is None
        BodyTarget(source1).apply(action, actions_list)
        assert action.body == b"v1"

        BodyTarget(source2).apply(action, actions_list)
        assert action.body == b"v2"

        # Test with a data source that returns a None value
        BodyTarget(source4).apply(action, actions_list)
        assert action.body == b"v2"

        assert action.url is None
        assert action.method is None
        assert action.cookies == []
        assert action.headers == dict()
