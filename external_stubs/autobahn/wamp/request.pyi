from _typeshed import Incomplete

__all__ = ['Publication', 'Subscription', 'Handler', 'Registration', 'Endpoint', 'PublishRequest', 'SubscribeRequest', 'UnsubscribeRequest', 'CallRequest', 'InvocationRequest', 'RegisterRequest', 'UnregisterRequest']

class Publication:
    id: Incomplete
    was_encrypted: Incomplete
    def __init__(self, publication_id, was_encrypted) -> None: ...

class Subscription:
    id: Incomplete
    topic: Incomplete
    active: bool
    session: Incomplete
    handler: Incomplete
    def __init__(self, subscription_id, topic, session, handler) -> None: ...
    def unsubscribe(self): ...

class Handler:
    fn: Incomplete
    obj: Incomplete
    details_arg: Incomplete
    def __init__(self, fn, obj: Incomplete | None = None, details_arg: Incomplete | None = None) -> None: ...

class Registration:
    id: Incomplete
    active: bool
    session: Incomplete
    procedure: Incomplete
    endpoint: Incomplete
    def __init__(self, session, registration_id, procedure, endpoint) -> None: ...
    def unregister(self): ...

class Endpoint:
    fn: Incomplete
    obj: Incomplete
    details_arg: Incomplete
    def __init__(self, fn, obj: Incomplete | None = None, details_arg: Incomplete | None = None) -> None: ...

class Request:
    request_id: Incomplete
    on_reply: Incomplete
    def __init__(self, request_id, on_reply) -> None: ...

class PublishRequest(Request):
    was_encrypted: Incomplete
    def __init__(self, request_id, on_reply, was_encrypted) -> None: ...

class SubscribeRequest(Request):
    topic: Incomplete
    handler: Incomplete
    def __init__(self, request_id, topic, on_reply, handler) -> None: ...

class UnsubscribeRequest(Request):
    subscription_id: Incomplete
    def __init__(self, request_id, on_reply, subscription_id) -> None: ...

class CallRequest(Request):
    procedure: Incomplete
    options: Incomplete
    def __init__(self, request_id, procedure, on_reply, options) -> None: ...

class InvocationRequest(Request): ...

class RegisterRequest(Request):
    procedure: Incomplete
    endpoint: Incomplete
    def __init__(self, request_id, on_reply, procedure, endpoint) -> None: ...

class UnregisterRequest(Request):
    registration_id: Incomplete
    def __init__(self, request_id, on_reply, registration_id) -> None: ...
