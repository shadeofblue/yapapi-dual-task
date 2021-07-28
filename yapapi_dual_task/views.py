import random
import string

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse

from yapapi import __version__ as yapapi_version

from .golem import Golem
from .golem.service import GolemService
from .forms import BlenderForm

GOLEM_CONFIG= {
    "budget": 0.1,
    "app_key": settings.YAGNA_APPKEY,
}


async def run(request: HttpRequest):
    golem = Golem(**GOLEM_CONFIG)
    await golem.start()

    service = GolemService(golem=golem.golem)
    await service.start()

    post = request.method == "POST"
    if post:
        form = BlenderForm(request.POST, request.FILES)
        if form.is_valid():
            print("FORM VALID", form.cleaned_data)

            output_dir = settings.BLENDER_OUTPUT_DIR
            output_filename = "".join(random.choice(string.ascii_letters) for _ in range(10)) + ".png"

            scene_file = request.FILES["scene_file"].temporary_file_path()
            result = await service.render_blender({
                "scene_file": scene_file,
                "x": form.cleaned_data["x"],
                "y": form.cleaned_data["y"],
                "frame": form.cleaned_data["frame"],
                "output_dir": output_dir,
                "output_filename": output_filename,
            })
            return TemplateResponse(
                request,
                "blender_out.html",
                {
                    "output_filename": result
                }
            )
    else:
        form = BlenderForm()

    return TemplateResponse(
        request,
        "blender.html",
        {
            "version": yapapi_version,
            "network": golem._golem.network,
            "driver": golem._golem.driver,
            "form": form,
            "post": post,
        }
    )
