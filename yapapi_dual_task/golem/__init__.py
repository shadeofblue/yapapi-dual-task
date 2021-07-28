from datetime import datetime


from yapapi import Golem as _Golem
from yapapi import log as yapapi_log


from .async_singleton import AsyncSingleton


class Golem(AsyncSingleton):
    def __init__(self, *args, **kwargs):
        if self._instance:
            return

        super().__init__(*args, **kwargs)

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
            await self._stack.enter_async_context(self._golem)

    @property
    def golem(self):
        return self._golem
