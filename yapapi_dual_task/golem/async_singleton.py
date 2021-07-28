import asyncio
from contextlib import AsyncExitStack
import signal

from .singleton import Singleton


class AsyncSingleton(Singleton):
    __instantiated_class = None
    _started: bool = False

    def __new__(cls, *args, **kwargs):
        if AsyncSingleton.__instantiated_class and AsyncSingleton.__instantiated_class != cls:
            raise Exception(f"Cannot have more than one AsyncSingleton class")
        AsyncSingleton.__instantiated_class = cls

        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        if self._instance:
            return

        super().__init__(*args, **kwargs)
        self._stack = AsyncExitStack()

    async def start(self):
        if self._started:
            return False

        self._started = True
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.stop()))
        return True

    async def stop(self):
        await self._stack.aclose()

    @classmethod
    def is_started(cls):
        return cls._instance and cls._instance._started
