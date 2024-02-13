####################################

# Taken from the official FIEF documenation: https://docs.fief.dev/integrate/python/fastapi/

# Imports

from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse
from fief_client import FiefAccessTokenInfo, FiefAsync
from fief_client.integrations.fastapi import FiefAuth

from config.settings import settings

# NiceGUI
import feng

####################################

# App

fief = FiefAsync(settings.fief_server_url, settings.fief_client_id, settings.fief_client_secret)

oauth2 = OAuth2AuthorizationCodeBearer(
    f"{settings.fief_server_url}/authorize",
    f"{settings.fief_server_url}/api/token",
    scopes={"openid": "openid", "offline_access": "offline_access"},
    auto_error=False,
)

auth = FiefAuth(fief, oauth2)

AuthenticatedUser = Annotated[FiefAccessTokenInfo, Depends(auth.authenticated())]

app = FastAPI()

####################################

# Route(s)

@app.get("/user")
async def get_user(
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    print(f"TokenInfo: {access_token_info}")
    return access_token_info

####################################

# NiceGUI
feng.init(app)
