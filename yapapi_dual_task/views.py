from django.conf import settings
from django.http import HttpRequest
from django.template.response import TemplateResponse

from yapapi import __version__ as yapapi_version

from .golem import Golem

GOLEM_CONFIG= {
    "budget": 0.1,
    "app_key": settings.YAGNA_APPKEY,
}


async def run(request: HttpRequest):
    golem = Golem(**GOLEM_CONFIG)
    await golem.start()
    return TemplateResponse(
        request,
        "blender.html",
        {"version": yapapi_version, "network": golem._golem.network, "driver": golem._golem.driver}
    )
