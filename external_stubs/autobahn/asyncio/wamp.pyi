from _typeshed import Incomplete
from autobahn.wamp import protocol

__all__ = ['ApplicationSession', 'ApplicationSessionFactory', 'ApplicationRunner']

class ApplicationSession(protocol.ApplicationSession):
    log: Incomplete

class ApplicationSessionFactory(protocol.ApplicationSessionFactory):
    session: ApplicationSession
    log: Incomplete

class ApplicationRunner:
    log: Incomplete
    url: Incomplete
    realm: Incomplete
    extra: Incomplete
    serializers: Incomplete
    ssl: Incomplete
    proxy: Incomplete
    headers: Incomplete
    def __init__(self, url, realm: Incomplete | None = None, extra: Incomplete | None = None, serializers: Incomplete | None = None, ssl: Incomplete | None = None, proxy: Incomplete | None = None, headers: Incomplete | None = None) -> None: ...
    def stop(self) -> None: ...
    def run(self, make, start_loop: bool = True, log_level: str = 'info'): ...

class Session(protocol._SessionShim):
    def on_welcome(self, welcome_msg) -> None: ...
    def on_join(self, details) -> None: ...
    def on_leave(self, details) -> None: ...
    def on_connect(self) -> None: ...
    def on_disconnect(self) -> None: ...
