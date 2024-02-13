from tempfile import NamedTemporaryFile

from cdprecorder.action import RequestAction, ResponseAction
from cdprecorder.datasource import HeaderSource, CookieSource, BodySource
from cdprecorder.datatarget import HeaderTarget, CookieTarget, BodyTarget
from cdprecorder.generate_python import write_python_code
from cdprecorder.http_types import Cookie


RES_DIR = 'tests/res/'
CODE_NO_ACTIONS_FILE = RES_DIR + "code_no_actions.py"
CODE_SIMPLE_ACTIONS_FILE = RES_DIR + "code_simple_actions.py"
CODE_COMPLEX_ACTIONS_FILE = RES_DIR + "code_complex_actions.py"


def get_file_contents(path: str) -> str:
    text = ""
    with open(path, "r") as f:
        text = f.read()

    return text
    

def test_write_python_code_no_actions():
    expected = get_file_contents(CODE_NO_ACTIONS_FILE)
    with NamedTemporaryFile() as file:
        write_python_code([], file.name)
        generated = get_file_contents(file.name)
        assert generated == expected


SIMPLE_ACTIONS = [
    RequestAction(
        method="POST",
        has_response=True,
    ),
    ResponseAction(
        status=302,
        body="test"
    ),
    RequestAction(
        method="GET",
        has_response=False,
    ),
]

def test_write_python_code_simple_actions():
    expected = get_file_contents(CODE_SIMPLE_ACTIONS_FILE)
    with NamedTemporaryFile() as file:
        write_python_code(SIMPLE_ACTIONS, file.name)
        generated = get_file_contents(file.name)
        assert generated == expected


COMPLEX_ACTIONS = [
    RequestAction(
        method="GET",
        url="http://test.com",
        headers={
            "user-agent": "Chrome",
        },
        has_response=True,
    ),
    ResponseAction(
        url="http://test.com",
        headers={
            "Test": "test",
            "X-Server": "apache12382193",
        },
        cookies={
            "XSRF-TOKEN": "gd76s8adghjsad7a",
            "test-session": "nn89dsahdsakjn%3D",
            "locale": "en-0.9",
        },
        status=200,
        body="test",
    ),
    RequestAction(
        method="POST",
        headers={
            "Test1": "test",
            "user-agent": "Chrome",
            "X-XSRF-TOKEN": "gd76s8adghjsad7a",
        },
        cookies=[
            Cookie("XSRF-TOKEN", "gd76s8adghjsad7a"),
            Cookie("test-session", "nn89dsahdsakjn%3D"),
            Cookie("locale", "en-0.9"),
        ],
        has_response=True,
    ),
    ResponseAction(
        status=200,
        body="Version9018238721783",
    ),
    RequestAction(
        method="GET",
        has_response=True,
        body="",
    ),
    ResponseAction(
        status=200,
        body="test",
    ),
    RequestAction(
        method="GET",
        headers={
            "X-Server-Resp": "apache12382193",
        },
        has_response=False,
        body="Version9018238721783",
    ),
]
COMPLEX_ACTIONS[2].targets.extend((
    HeaderTarget(CookieSource(1, "XSRF-TOKEN", ".*"), "X-XSRF-TOKEN", "gd76s8adghjsad7a"),
    CookieTarget("XSRF-TOKEN", CookieSource(1, "XSRF-TOKEN", ".*")),
    CookieTarget("test-session", CookieSource(1, "test-session", ".*")),
))
COMPLEX_ACTIONS[6].targets.extend((
    HeaderTarget(HeaderSource(1, "x-server"), "x-server-resp", "apache12382193"),
    BodyTarget(BodySource(3)),
))

def test_write_python_code_complex_actions():
    expected = get_file_contents(CODE_COMPLEX_ACTIONS_FILE)
    with NamedTemporaryFile() as file:
        write_python_code(COMPLEX_ACTIONS, file.name)
        generated = get_file_contents(file.name)
        assert generated == expected
