from django.conf import settings
from django.http import HttpResponse, HttpRequest

from .golem import Golem

GOLEM_CONFIG= {
    "budget": 0.1,
    "app_key": settings.YAGNA_APPKEY,
}


async def run(request: HttpRequest):
    golem = Golem(**GOLEM_CONFIG)
    await golem.start()
    return HttpResponse(golem._golem.network)
