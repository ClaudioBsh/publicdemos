####################################

# Parts taken from:
#             https://nicegui.io
#             https://nicegui.io/documentation/section_configuration_deployment
#             https://github.com/zauberzeug/nicegui/tree/main/examples/fastapi/
#             https://github.com/markbaumgarten/nicegui-letsencrypt/blob/main

# Why naming 'FENG'? => FrontEndNiceGui = FENG

# Imports

import os
import requests

from nicegui import app, ui
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from config.settings import settings

# Init

fief_base_url=settings.fief_server_url
api_url=f'{fief_base_url}:8000'
my_redirect_uri = '{fief_base_url}8000/public'


static_files = StaticFiles(
    directory=(Path(__file__).parent / 'static').resolve(),
    follow_symlink=True,
)
app.mount('/static', static_files, name='static')

def init(fastapi_app: FastAPI) -> None:
    @ui.page('/')
    async def main_page(request: Request) -> None:
        return RedirectResponse('/public')

    ui.run_with(
        fastapi_app,
    )

def check_authentication():
    response = requests.get(f'{api_url}/private', cookies=ui.request.cookies)
    if response.status_code == 200:
        return response.json()
    else:
        return None

####################################

# Page(s)

def on_private_page():
    user = check_authentication()
    ui.clear()
    with ui.page('/private'):
        if user:
            ui.label(f'Private Page - Welcome: {user["email"]}')
            ui.button('Back to public page', on_click=lambda: ui.goto('/'))
        else:
            ui.notify('Access denied. Please login.', level='error')
            ui.goto('/')

@ui.page('/public')
async def info(request: Request) -> None:
    with ui.header().classes('bg-transparent'), ui.column().classes('w-full max-w-3xl mx-auto my-3'):
        ui.image('/static/logo.png').classes('max-w-[20%]')
    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        ui.label("""Hello NiceGUI World""")
    ui.label('Publice Page')
    ui.button('Call private endpoint (needs authentification)', on_click=on_private_page)
    ui.button('Login', on_click=lambda: ui.redirect(f'{fief_base_url}/auth/login?redirect_uri={my_redirect_uri}'))
    ui.button('Register', on_click=lambda: ui.redirect(f'{fief_base_url}/auth/register?redirect_uri={my_redirect_uri}'))

####################################
