from _typeshed import Incomplete
from autobahn import xbr as xbr
from autobahn.util import hl as hl
from autobahn.xbr._interfaces import IBuyer as IBuyer, IConsumer as IConsumer, IProvider as IProvider, ISeller as ISeller

HAS_XBR: bool

def run_in_executor(*args, **kwargs): ...

class SimpleBlockchain(xbr.SimpleBlockchain):
    backgroundCaller = run_in_executor

class KeySeries(xbr.KeySeries):
    log: Incomplete
    running: bool
    def __init__(self, api_id, price, interval, on_rotate: Incomplete | None = None) -> None: ...
    async def start(self) -> None: ...
    def stop(self) -> None: ...

class SimpleSeller(xbr.SimpleSeller): ...
class SimpleBuyer(xbr.SimpleBuyer): ...
