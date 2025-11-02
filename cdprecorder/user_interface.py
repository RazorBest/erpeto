import abc
from typing import TYPE_CHECKING, Callable

from twisted.internet.interfaces import IReactorCore

if TYPE_CHECKING:
    from typing import TYPE_CHECKING, Callable
    from twisted.internet.interfaces import IReactorCore


class RecordControlUI(abc.ABC):
    @abc.abstractmethod
    def __init__(self, event_loop: IReactorCore, on_start: Callable[[], None], on_stop: Callable[[], None]):
        pass
