import json
import pytest

from unittest.mock import patch

from .mocks import EventMock, UrlfilterMock
from .action_serializer import replace_action_body_with_length, replace_date_headers, ActionsJSONEncoder, json_actions_loads

import cdprecorder
from main import parse_communications_into_actions
from cdprecorder.recorder import collect_communications, set_runtime_context


@pytest.mark.parametrize(
    "events_file, actions_file", 
    [
        (
            "tests/events_youtube.json",
            "tests/actions_youtube.json",
        ),
    ],
)
@pytest.mark.asyncio
@patch("cdprecorder.recorder.RuntimeContext")
async def test_parse_communications_into_actions(RuntimeContext, events_file, actions_file):
    with open(events_file, encoding="utf8") as f:
        events = json.load(f)
    with open(actions_file, encoding="utf8") as f:
        expected_actions = json_actions_loads(f.read())

    event_mock = EventMock(events)
    urlfilter = UrlfilterMock()
    set_runtime_context(RuntimeContext())

    communications = await collect_communications(event_mock, 
        event_mock, urlfilter, timeout=10, collect_all=True)
    
    set_runtime_context(None)

    actions = parse_communications_into_actions(communications)

    for action in actions:
        replace_action_body_with_length(action)

    assert actions == expected_actions
