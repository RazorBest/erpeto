import dateutil
import json

from dataclasses import dataclass

from ..main import Cookie, BrowserAction, HttpAction, RequestAction, ResponseAction

@dataclass
class LengthBody:
    length: int = 0
    def __init__(self, body=None, length=None):
        if body is not None:
            self.length = len(body)
        elif length is not None:
            self.length = length
        

class DummyDate:
    pass


class HttpBody:
    def __init__(self, body):
        self.is_base64 = False
        if isinstance(body, str):
            self.body = body
            return

        self.is_base64 = True
        self.body = base64.b64encode(body).decode("utf8")

    def __len__(self):
        if isinstance(body, str):
            return len(self.body.encode())

        if self.is_base64:
            return len(base64.b64decode(self.body))


class ActionsJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cookie):
            return vars(obj) | {"_pytype": obj.__class__.__name__}
        if isinstance(obj, BrowserAction):
            return vars(obj) | {"_pytype": obj.__class__.__name__}
        if isinstance(obj, HttpBody):
            return {"_pytype": obj.__class__.__name__, "is_base64": obj.is_base64, "body": obj.body}
        if isinstance(obj, LengthBody):
            return {"_pytype": obj.__class__.__name__, "length": obj.length}
        if isinstance(obj, DummyDate):
            return {"_pytype": obj.__class__.__name__}
        if isinstance (obj, bytes):
            wrapper = HttpBody(obj)
            return {"_pytype": HttpBody, "is_base64": wrapper.is_base64, "body": wrapper.body}

        return json.JSONEncoder.default(self, obj)


def typed_object_hook(obj):
    """Warning: this function instanciates python objects from classes in the
    global namespace. If it receives an untrusted dict, this might lead to
    unwanted instantiations or even code injection."""
    if not isinstance(obj, dict) or "_pytype" not in obj:
        return obj

    # Buckle up, ugly code in 5 meters
    if obj["_pytype"] not in globals():
        raise LookupError(obj["_pytype"])
    cls = globals()[obj["_pytype"]]
    if not isinstance(cls, type):
        raise LookupError(obj["_pytype"])

    if obj["_pytype"] == "Cookie":
        return Cookie(
            name=obj["name"],
            value=obj["value"],
            expires=obj["expires"],
            path=obj["path"],
            samesite=obj["samesite"],
            httponly=obj["httponly"],
        )
    if issubclass(cls, HttpAction):
        if obj["_pytype"] == "RequestAction":
            action = RequestAction()
            action.has_response = obj["has_response"]
        elif obj["_pytype"] == "ResponseAction":
            action = ResponseAction()
            action.status = obj["status"]
        action.method = obj["method"]
        action.headers = obj["headers"]
        action.url = obj["url"]
        action.body = obj["body"]
        action.cookies = obj["cookies"]
        return action
    if obj["_pytype"] == "HttpBody":
        if obj["is_base64"]:
            return base64.b64decode(obj["body"])
        return obj["body"]
    if obj["_pytype"] == "LengthBody":
        return LengthBody(length=obj["length"])
    if obj["_pytype"] == "DummyDate":
        return DummyDate()

    raise LookupError(obj["_pytype"])


def json_actions_loads(text: str):
    """Warning: this function instanciates python objects from classes in the
    global namespace. If it receives an untrusted string, this might lead to
    unwanted instantiations or event code injection."""
    return json.loads(text, object_hook=typed_object_hook)


def replace_action_body_with_length(action):
    if action.body is None:
        return action
    action.body = LengthBody(action.body)
    return action


def is_date(string, fuzzy=False):
    # ints and floats are not considered dates
    try:
        float(string)
        return False
    except ValueError:
        pass

    try:
        dateutil.parser.parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def replace_date_headers(action, replacement=None):
    headers = action.headers
    for key in headers:
        if not is_date(headers[key]):
            continue
        if replacement is not None:
            headers[key] = replacement
        else:
            headers[key] = DummyDate()
    return action
