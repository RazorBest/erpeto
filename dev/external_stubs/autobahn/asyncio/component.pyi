from _typeshed import Incomplete
from autobahn.asyncio.wamp import Session
from autobahn.wamp import component

__all__ = ['Component', 'run']

class Component(component.Component):
    log: Incomplete
    session_factory = Session
    def start(self, loop: Incomplete | None = None): ...

def run(components, start_loop: bool = True, log_level: str = 'info'): ...
