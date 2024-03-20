####################################

# Imports

from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import Fief, FiefAccessTokenInfo, FiefAsync
from fief_client.integrations.fastapi import FiefAuth

from config.settings import settings

# NiceGUI
import feng

####################################

# App

FIEF_SERVER_URL=settings.fief_server_url,
FIEF_CLIENT_ID=settings.fief_client_id,
FIEF_CLIENT_SECRET=settings.fief_client_secret,

fief = FiefAsync(
    FIEF_SERVER_URL,
    FIEF_CLIENT_ID,
    FIEF_CLIENT_SECRET,
#    host="localhost:8000",
)
oauth2 = OAuth2AuthorizationCodeBearer(
    f"{FIEF_SERVER_URL}/authorize",
    f"{FIEF_SERVER_URL}/api/token",
    scopes={"openid": "openid", "offline_access": "offline_access"},
    auto_error=False,
)
auth = FiefAuth(fief, oauth2)
# AuthenticatedUser = Annotated[FiefAccessTokenInfo, Depends(auth.authenticated())]

app = FastAPI()

####################################

# Route(s)

@app.get("/user")
async def get_user(
    user: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    print(f"TokenInfo: {user}")
    return user

# Public endpoint - does not need any authentification
@app.get("/public")
def read_public_data():
    return {"message": "This is a public page."}

# Private secured endpoint - needs authentification
@app.get("/private")
async def read_private_data(user: FiefAccessTokenInfo = Depends(auth.authenticated())):

    return {"message": f"Secret (private) page - you are authenticated as: {user.email}"}

####################################

# NiceGUI
feng.init(app)
