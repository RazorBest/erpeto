import json
import pytest

from unittest.mock import patch

from .conftest import DummyDataSource

from cdprecorder.action import (
    LowercaseStr,
    RequestAction,
    ResponseAction,
)
from cdprecorder.datasource import (
    CookieSource,
    HeaderSource,
    JSONContainer,
    JSONFieldTarget,
    SubstrSource,
    StrSource,
)
from cdprecorder.http_types import Cookie


class TestSubstrSource:
    def test_get_value(self):
        source = SubstrSource(StrSource("test11"), start=1, end=4)
        assert source.get_value([]) == "est"

        source = SubstrSource(
            SubstrSource(StrSource("tttest2222"), start=1, end=7),
            start=1, end=6,
        )
        assert source.get_value([]) == "test2"

        source = SubstrSource(
            SubstrSource(
                SubstrSource(
                    StrSource("other_tests3"),
                    start=2, end=9,
                ),
                start=0, end=-1,
            ),
            start=1, end=1000,
        )
        assert source.get_value([]) == "er_te"


@pytest.fixture()
def actions_list():
    action1 = ResponseAction(
        headers={
            LowercaseStr("User-Agent"): "Chrome",
            LowercaseStr("Test1"): "test",
            LowercaseStr("Time"): "12:06:29",
        },
        cookies=[
            Cookie("session", "test"),
            Cookie("_gl", "1.0.21879"),
        ],
        body='{"json_key": [{"key3": "test"}, "test2", 2, false], "key2": none}',
    ) 
    action2 = ResponseAction(headers={
        LowercaseStr("User-Agent"): "Chrome",
        LowercaseStr("Test2"): "test",
        LowercaseStr("Time"): "12:06:30",
    }) 
    action3 = ResponseAction(
        headers={
            LowercaseStr("User-Agent"): "Chrome",
            LowercaseStr("Test3"): "test",
            LowercaseStr("X-Link"): "url",
        },
        cookies=[
            Cookie("session", "test2"),
            Cookie("_gl2", "1.0.12368"),
        ],
        # Invalid JSON
        body='{"json_key": [{"key3": "test"}, "test2", 2, false, "key2": none}',
    ) 

    actions = [action1, action2, action3]

    yield actions


class TestHeaderSource:
    def test_get_value(self, actions_list):
        source = HeaderSource(0, "user-Agent")
        value = source.get_value(actions_list)
        assert value == "Chrome"

        source = HeaderSource(1, "time")
        value = source.get_value(actions_list)
        assert value == "12:06:30"

        source = HeaderSource(2, "time")
        value = source.get_value(actions_list)
        assert value == None


class TestCookieSource:
    def test_get_value(self, actions_list):
        source = CookieSource(0, "session", ".*")
        value = source.get_value(actions_list)
        assert value == "test"

        import re
        source = CookieSource(2, "_gl2", r".*")
        value = source.get_value(actions_list)
        assert value == "1.0.12368"

        source = CookieSource(2, "inexistent", ".*")
        value = source.get_value(actions_list)
        assert value == None

        source = CookieSource(1, "session", ".*")
        value = source.get_value(actions_list)
        assert value == None


class SchemaDummy:
    def __init__(self, data):
        self.data = data


class TestFieldTarget:
    def test_apply(self, actions_list):
        source = DummyDataSource("expected")
        body = '{"json_key": [{"key3": "test"}, "test2", 2, false], "key2": null}'

        data = json.loads(body)
        target = JSONFieldTarget(source, ["json_key"])
        target.apply(data, actions_list)
        assert data == {"json_key": "expected", "key2": None}

        data = json.loads(body)
        target = JSONFieldTarget(source, ["json_key", 0, "key3"])
        target.apply(data, actions_list)
        assert data == {"json_key": [{"key3": "expected"}, "test2", 2, False], "key2": None}

        data = json.loads(body)
        target = JSONFieldTarget(source, ["json_key", 1])
        target.apply(data, actions_list)
        assert data == {"json_key": [{"key3": "test"}, "expected", 2, False], "key2": None}

        data = json.loads(body)
        target = JSONFieldTarget(source, ["json_key", 2])
        target.apply(data, actions_list)
        assert data == {"json_key": [{"key3": "test"}, "test2", "expected", False], "key2": None}

        data = json.loads(body)
        target = JSONFieldTarget(source, ["json_key", 3])
        target.apply(data, actions_list)
        assert data == {"json_key": [{"key3": "test"}, "test2", 2, "expected"], "key2": None}

        data = json.loads(body)
        target = JSONFieldTarget(source, ["key2"])
        target.apply(data, actions_list)
        assert data == {"json_key": [{"key3": "test"}, "test2", 2, False], "key2": "expected"}

        data = json.loads(body)
        target = JSONFieldTarget(source, [])
        target.apply(data, actions_list)
        assert data == json.loads(body)

        # The following tests cases of invalid paths

        data = json.loads(body)
        target = JSONFieldTarget(source, ["key3"])
        target.apply(data, actions_list)
        assert data == json.loads(body)

        data = json.loads(body)
        target = JSONFieldTarget(source, ["json_key", 100])
        target.apply(data, actions_list)
        assert data == json.loads(body)

        data = json.loads(body)
        target = JSONFieldTarget(source, ["json_key", 0, "key3", 2])
        target.apply(data, actions_list)
        assert data == json.loads(body)

        data = json.loads(body)
        target = JSONFieldTarget(source, ["json_key", 1, "invalid"])
        target.apply(data, actions_list)
        assert data == json.loads(body)

        data = json.loads(body)
        target = JSONFieldTarget(source, ["json_key", 2, 0])
        target.apply(data, actions_list)
        assert data == json.loads(body)

        data = json.loads(body)
        target = JSONFieldTarget(source, ["json_key", 3, 0])
        target.apply(data, actions_list)
        assert data == json.loads(body)

        target = JSONFieldTarget(source, ["key2", 0])
        target.apply(data, actions_list)
        assert data == json.loads(body)

        target = JSONFieldTarget(source, ["key2", "invalid"])
        target.apply(data, actions_list)
        assert data == json.loads(body)


class TestJsonContainer:
    def test_get_value(self, actions_list):
        body='{"json_key": [{"key3": "test"}, "test2", 2, false], "key2": null}'
        schema = SchemaDummy(json.loads(body))
        source1 = DummyDataSource("a1")
        source2 = DummyDataSource("a2")
        source3 = DummyDataSource("a3")

        targets = [
            JSONFieldTarget(source1, ["json_key", 0, "key3"]),
            JSONFieldTarget(source2, ["key2"]),
            JSONFieldTarget(source3, ["json_key", 1]),
            JSONFieldTarget(source1, ["json_key", 2]),
        ]
        container = JSONContainer(schema, targets)

        value = container.get_value(actions_list)
        assert value == '{"json_key": [{"key3": "a1"}, "a3", "a1", false], "key2": "a2"}'

