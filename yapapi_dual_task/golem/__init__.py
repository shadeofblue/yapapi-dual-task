import asyncio
from datetime import datetime


from yapapi import Golem as _Golem, __version__ as golem_version
from yapapi import log as yapapi_log


from .async_singleton import AsyncSingleton


class Golem(AsyncSingleton):
    def __init__(self, *args, **kwargs):
        if self._instance:
            return

        super().__init__(*args, **kwargs)

        print(f"------------------------------- GOLEM INIT {args, kwargs}, "
              f"yapapi version {golem_version}")

        now = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

        yapapi_log.enable_default_logger(
            log_file=f"dual-task-yapapi-{now}.log",
            debug_activity_api=True,
            debug_market_api=True,
            debug_payment_api=True,
        )

        self._golem = _Golem(*args, **kwargs)

    async def start(self):
        if await super().start():
            print("------------------------------- STARTING GOLEM")

            loop = asyncio.get_event_loop()
            task = loop.create_task(self._stack.enter_async_context(self._golem))
            while not task.done():
                await asyncio.sleep(0.1)

            print("------------------------------- GOLEM STARTED")

    async def stop(self):
        print("------------------------------- STOPPING GOLEM")
        await super().stop()
        print("------------------------------- GOLEM STOPPED")

