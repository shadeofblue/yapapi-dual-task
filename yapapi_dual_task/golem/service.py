import asyncio
from datetime import timedelta
import pathlib
import tempfile


from yapapi import Task, Golem
from yapapi.ctx import WorkContext
from yapapi.payload import vm
from yapapi.rest.activity import BatchTimeoutError

from .async_singleton import AsyncSingleton


class GolemService(AsyncSingleton):
    blender_payload = None
    date_payload = None
    blender_queue = None

    def __init__(self, golem: Golem):
        if self._instance:
            return

        super().__init__()
        self.golem = golem

    async def start(self):
        if not await super().start():
            return

        # self.date_payload = await vm.repo(
        #     image_hash="d646d7b93083d817846c2ae5c62c72ca0507782385a2e29291a3d376",
        # )

        print("STARTING BLENDER SERVICE")
        self.blender_queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        loop.create_task(self.blender_task())

    @staticmethod
    async def blender_worker(ctx: WorkContext, tasks):
        async for task in tasks:
            print("------------------ BLENDER WORKER TASK", task, task.data)

            params = task.data["params"]
            ctx.send_file(params["scene_file"], "/golem/resource/scene.blend")
            frame = int(params["frame"])
            crops = [{"outfilebasename": "out", "borders_x": [0.0, 1.0], "borders_y": [0.0, 1.0]}]
            ctx.send_json(
                "/golem/work/params.json",
                {
                    "scene_file": "/golem/resource/scene.blend",
                    "resolution": (int(params["x"]), int(params["y"])),
                    "use_compositing": False,
                    "crops": crops,
                    "samples": 100,
                    "frames": [frame],
                    "output_format": "PNG",
                    "RESOURCES_DIR": "/golem/resources",
                    "WORK_DIR": "/golem/work",
                    "OUTPUT_DIR": "/golem/output",
                },
            )
            ctx.run("/golem/entrypoints/run-blender.sh")
            output_file = params["output_dir"] / params["output_filename"]
            ctx.download_file(f"/golem/output/out{frame:04d}.png", output_file)
            try:
                yield ctx.commit(timeout=timedelta(minutes=10))
                task.accept_result(result=params["output_filename"])
            except BatchTimeoutError:
                raise

    async def blender_task(self):

        print("BLENDER TASK STARTED")

        async def tasks():
            print("BLENDER TASKS GENERATOR STARTED")
            while True:
                future, blender_params = await self.blender_queue.get()
                print(f"------------------ blender single: {blender_params}")
                yield Task(data={"params": blender_params, "result": future})

        async for completed in self.golem.execute_tasks(
            worker=self.blender_worker,
            data=tasks(),
            payload=await vm.repo(
                image_hash="9a3b5d67b0b27746283cb5f287c13eab1beaa12d92a9f536b747c7ae",
                min_mem_gib=0.5,
                min_storage_gib=2.0,
            ),
            timeout=timedelta(minutes=10),
        ):
            print("TASK COMPLETED", completed)
            completed.data["result"].set_result(completed.result)

    async def render_blender(self, params):
        print("RENDER BLENDER")
        loop = asyncio.get_event_loop()
        f = loop.create_future()
        self.blender_queue.put_nowait((f, params))
        return await f