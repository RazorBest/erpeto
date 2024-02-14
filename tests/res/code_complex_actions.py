from __future__ import annotations
import re
import requests
import urllib

from requests import Session
from abc import ABC, abstractmethod


class LowercaseStr(str):
    def __new__(cls, value: str, *args: object, **kwargs: object) -> LowercaseStr:
        return super(LowercaseStr, cls).__new__(cls, value.lower(), *args, **kwargs)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(str(other).lower())

    def __hash__(self) -> int:
        return super().__hash__()


class Cookie:
    def __init__(self, name = "", value = ""):
        self.name = name
        self.value = value

    def to_dict(self):
        return {self.name: self.value}

    @classmethod
    def list_from_cookiejar(cls, cookie_jar):
        cookies = []
        for cookie in cookie_jar:
            obj = cls(
                getattr(cookie, "name", ""),
                getattr(cookie, "value", ""),
            )
            cookies.append(obj)

        return cookies


class RequestAction:
    def __init__(self, method=None, url=None, headers=None, body=None, cookies=None, has_response=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.body = body
        self.has_response = has_response

    def cookies_to_dict(self) -> dict[str, str]:
        cookie_dict = {}
        for cookie in self.cookies:
            cookie_dict.update(cookie.to_dict())

        return cookie_dict


class ResponseAction:
    def __init__(self, url=None, headers=None, body=None, cookies=None, status=None):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.body = body
        self.status = status


class IntermediaryDataSource:
    def __init__(self, upper_source):
        self.upper_source = upper_source

    def get_value(self, prev_actions):
        upper_source_value = self.upper_source.get_value(prev_actions)
        return get_value_from_upper_value(self.upper_source)


class DataSource(ABC, ReprSource):
    @abstractmethod
    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        pass


class IntermediaryDataSource:
    def __init__(self, upper_source: DataSource) -> None:
        self.upper_source = upper_source

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        upper_source_value = self.upper_source.get_value(prev_actions)
        return self.get_value_from_upper_value(upper_source_value)

    @abstractmethod
    def get_value_from_upper_value(self, upper_value: str) -> Optional[str]:
        pass


class JSONSource(DataSource):
    def __init__(self, data: str, token_classifier: Optional[Callable[[str], bool]] = None):
        self.data = json.loads(data)

        if token_classifier is not None:
            self.classifier = token_classifier
        else:
            self.classifier = lambda token: randomness_score(token) >= 50

        self.targets: list[JSONField] = []
        self.classify_tokens()

    def _classify(self, data: object, path: list[Union[str, int]]) -> list[JSONField]:
        targets = []
        if isinstance(data, dict):
            for key, val in data.items():
                targets += self._classify(val, path + [key])
        elif isinstance(data, list):
            for index, val in enumerate(data):
                targets += self._classify(val, path + [index])
        elif isinstance(data, str):
            if self.classifier(data):
                target = JSONField(data, path)
                targets.append(target)
        # TODO: decide for int, bool, bytes etc

        return targets

    def classify_tokens(self) -> None:
        self.targets = self._classify(self.data, [])

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> str:
        for field_target in self.targets:
            if not field_target.source:
                continue
            field_target.apply(self.data, prev_actions)

        return json.dumps(self.data)


class StrSource(DataSource):
    def __init__(self, text: str) -> None:
        self.text = text

    def get_value(self, prev_actions: Sequence[Optional[HttpAction]]) -> Optional[str]:
        return self.text


class BodyTarget(SingleSourcedTarget):
    def apply_value(self, action: HttpAction, value:str) -> None:
        action.body = value.encode()


class CookieTarget(SingleSourcedTarget):
    def __init__(self, name: str, source: DataSource):
        super().__init__(source)
        self.name = name

    def apply_value(self, action: HttpAction, value: str) -> None:
        for cookie in action.cookies:
            if cookie.name == self.name:
                cookie.value = value
                break
        else:
            action.cookies.append(Cookie(self.name, value))


class HeaderTarget(SingleSourcedTarget):
    def __init__(self, source: DataSource, key: str, value: str):
        super().__init__(source)
        self.key = LowercaseStr(key)
        self.value = value

    def apply_value(self, action: HttpAction, value: str) -> None:
        action.headers[self.key] = value


class SingleSourcedTarget(ABC):
    def __init__(self, source: DataSource):
        self.source = source

    def apply(self, action: HttpAction, prev_actions: list[Optional[HttpAction]]) -> None:
        value = self.source.get_value(prev_actions)
        if value is None:
            return
        self.apply_value(action, value)

    @abstractmethod
    def apply_value(self, action: HttpAction, value: str) -> None:
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

REQUEST_BODY_4 = ''
REQUEST_BODY_6 = 'Version9018238721783'


actions = []

action_0 = RequestAction(
    method='GET',
    url='http://test.com',
    headers={
        'user-agent': 'Chrome',
    },
    cookies=[],
    body=None,
    has_response=True,
)
actions.append(action_0)
prepared_request_0 = requests.Request(
    method='GET',
    url='http://test.com',
    headers=action_0.headers,
    data=action_0.body,
    cookies=action_0.cookies_to_dict(),
).prepare()
response_0 = Session().send(prepared_request_0, allow_redirects=False)
actions.append(response_action_from_python_response(response_0))

action_2 = RequestAction(
    method='POST',
    url=None,
    headers={
        'Test1': 'test',
        'user-agent': 'Chrome',
        'X-XSRF-TOKEN': 'gd76s8adghjsad7a',
    },
    cookies=[
        Cookie('XSRF-TOKEN', 'gd76s8adghjsad7a'),
        Cookie('test-session', 'nn89dsahdsakjn%3D'),
        Cookie('locale', 'en-0.9'),
    ],
    body=None,
    has_response=True,
)
actions.append(action_2)
HeaderTarget(source=CookieSource(index=1, name='XSRF-TOKEN', strcontext='.*'), key='x-xsrf-token', value='gd76s8adghjsad7a').apply(action_2, actions)
CookieTarget(name='XSRF-TOKEN', source=CookieSource(index=1, name='XSRF-TOKEN', strcontext='.*')).apply(action_2, actions)
CookieTarget(name='test-session', source=CookieSource(index=1, name='test-session', strcontext='.*')).apply(action_2, actions)
prepared_request_2 = requests.Request(
    method='POST',
    url=None,
    headers=action_2.headers,
    data=action_2.body,
    cookies=action_2.cookies_to_dict(),
).prepare()
response_2 = Session().send(prepared_request_2, allow_redirects=False)
actions.append(response_action_from_python_response(response_2))

action_4 = RequestAction(
    method='GET',
    url=None,
    headers={},
    cookies=[],
    body=REQUEST_BODY_4,
    has_response=True,
)
actions.append(action_4)
prepared_request_4 = requests.Request(
    method='GET',
    url=None,
    headers=action_4.headers,
    data=action_4.body,
    cookies=action_4.cookies_to_dict(),
).prepare()
response_4 = Session().send(prepared_request_4, allow_redirects=False)
actions.append(response_action_from_python_response(response_4))

action_6 = RequestAction(
    method='GET',
    url=None,
    headers={
        'X-Server-Resp': 'apache12382193',
    },
    cookies=[],
    body=REQUEST_BODY_6,
    has_response=False,
)
actions.append(action_6)
HeaderTarget(source=HeaderSource(index=1, key='x-server'), key='x-server-resp', value='apache12382193').apply(action_6, actions)
BodyTarget(source=BodySource(index=3)).apply(action_6, actions)
prepared_request_6 = requests.Request(
    method='GET',
    url=None,
    headers=action_6.headers,
    data=action_6.body,
    cookies=action_6.cookies_to_dict(),
).prepare()
response_6 = Session().send(prepared_request_6, allow_redirects=False)
