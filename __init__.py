import asyncio

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

from lnbits.db import Database
from lnbits.helpers import template_renderer
from lnbits.tasks import catch_everything_and_restart

db = Database("ext_strike")


strike_ext: APIRouter = APIRouter(prefix="/strike", tags=["strike"])

strike_static_files = [
    {
        "path": "/strike/static",
        "app": StaticFiles(directory="lnbits/extensions/strike/static"),
        "name": "strike_static",
    }
]

def strike_renderer():
    return template_renderer(["lnbits/extensions/strike/templates"])

from .tasks import wait_for_paid_invoices
from .views import *  # noqa
from .views_api import *  # noqa


def strike_start():
    loop = asyncio.get_event_loop()
    loop.create_task(catch_everything_and_restart(wait_for_paid_invoices))
