####################################

# Taken from: https://nicegui.io
#             https://nicegui.io/documentation/section_configuration_deployment
#             https://github.com/zauberzeug/nicegui/tree/main/examples/fastapi/
#             https://github.com/markbaumgarten/nicegui-letsencrypt/blob/main

# Why naming 'FENG'? => FrontEndNiceGui = FENG

# Imports

import os

from nicegui import app, ui
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# Init

static_files = StaticFiles(
    directory=(Path(__file__).parent / 'static').resolve(),
    follow_symlink=True,
)
app.mount('/static', static_files, name='static')

def init(fastapi_app: FastAPI) -> None:
    @ui.page('/')
    async def main_page(request: Request) -> None:
        return RedirectResponse('/info')

    ui.run_with(
        fastapi_app,
    )

####################################

# Page(s)

@ui.page('/info')
async def info(request: Request) -> None:
    with ui.header().classes('bg-transparent'), ui.column().classes('w-full max-w-3xl mx-auto my-3'):
        ui.image('/static/logo.png').classes('max-w-[20%]')
    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        ui.label("""Hello NiceGUI World""")

####################################
