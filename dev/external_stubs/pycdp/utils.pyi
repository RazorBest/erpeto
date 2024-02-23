import typing as t
from pycdp.base import IEventLoop as IEventLoop

class LoggerMixin:
    def __init__(self, *args, **kwargs) -> None: ...

class ContextLoggerMixin(LoggerMixin):
    def __init__(self, *args, **kwargs) -> None: ...
    def set_logger_context(self, **context) -> None: ...

class DoneTask:
    def done(self): ...
    def cancel(self) -> None: ...

class Retry(LoggerMixin):
    def __init__(self, func, exception_class: t.Collection[BaseException], loop: IEventLoop, *, retries: int = 1, on_error: t.Optional[t.Union[str, t.Callable[[], t.Awaitable[None]]]] = None, log_errors: bool = False) -> None: ...
    async def __call__(self, *args, **kwargs): ...

class DelayedRetry(Retry):
    def __init__(self, delay: float, delay_growth: float, max_delay: float, **kwargs) -> None: ...

class RandomDelayedRetry(DelayedRetry): ...

def retry_on(*exception_class: t.Type[BaseException], loop: IEventLoop, retries: int = 1, delay: t.Union[float, t.Tuple[float, float]] = 0.0, delay_growth: float = 1.0, max_delay: int = 600, log_errors: bool = False, on_error: t.Optional[str] = None): ...

class Closable(LoggerMixin):
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def is_open(self): ...
    @property
    def closed(self): ...
    async def wait_closed(self) -> None: ...
    async def close(self) -> None: ...

class WorkerBase(Closable):
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def is_open(self): ...
    def start(self) -> None: ...
    async def close(self) -> None: ...

class SubtaskSpawner(Closable):
    def __init__(self, *args, **kwargs) -> None: ...
    async def wait_exception(self) -> None: ...
    async def wait_subtasks(self): ...

class Worker(SubtaskSpawner, WorkerBase):
    def __init__(self, *args, **kwargs) -> None: ...
    async def close_on_exception(self, exc: Exception): ...

class SingleTaskWorker(Worker): ...