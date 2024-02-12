import pytest

from unittest.mock import patch

from cdprecorder.action import (
    LowercaseStr,
    RequestAction,
    ResponseAction,
)
from cdprecorder.datasource import (
    HeaderSource,
    SubstrSource,
    StrSource,
)


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
    action1 = ResponseAction(headers={
        LowercaseStr("User-Agent"): "Chrome",
        LowercaseStr("Test1"): "test",
        LowercaseStr("Time"): "12:06:29",
    }) 
    action2 = ResponseAction(headers={
        LowercaseStr("User-Agent"): "Chrome",
        LowercaseStr("Test2"): "test",
        LowercaseStr("Time"): "12:06:30",
    }) 
    action3 = RequestAction(),
    action3 = ResponseAction(headers={
        LowercaseStr("User-Agent"): "Chrome",
        LowercaseStr("Test3"): "test",
        LowercaseStr("X-Link"): "url",
    }) 
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
