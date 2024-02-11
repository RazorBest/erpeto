import typing as t

class IEventLoop(t.Protocol):
    async def sleep(self, delay: float) -> None: ...
