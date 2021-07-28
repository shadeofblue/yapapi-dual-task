import asyncio
from contextlib import AsyncExitStack
from datetime import datetime
import signal
from typing import Optional


from yapapi import Golem as _Golem, __version__ as golem_version
from yapapi import log as yapapi_log


class Golem:
    __instance: Optional["Golem"] = None
    _started: bool = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        if self.__instance:
            return

        print(f"------------------------------- GOLEM INIT {args, kwargs}, "
              f"yapapi version {golem_version}")
        self._stack = AsyncExitStack()

        now = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

        yapapi_log.enable_default_logger(
            log_file=f"dual-task-yapapi-{now}.log",
            debug_activity_api=True,
            debug_market_api=True,
            debug_payment_api=True,
        )

        self._golem = _Golem(*args, **kwargs)
        Golem.__instance = self

    async def start(self):
        if self._started:
            return

        self._started = True
        print("------------------------------- STARTING GOLEM")
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._stack.enter_async_context(self._golem))
        while not task.done():
            await asyncio.sleep(0.1)

        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.stop()))

        print("------------------------------- GOLEM STARTED")

    async def stop(self):
        print("------------------------------- STOPPING GOLEM")
        await self._stack.aclose()
        print("------------------------------- GOLEM STOPPED")

    @classmethod
    def is_started(cls):
        return cls.__instance and cls.__instance._started
