from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import FiefAccessTokenInfo, FiefAsync
from fief_client.integrations.fastapi import FiefAuth

from config.settings import settings

fief = FiefAsync(settings.fief_server_url, settings.fief_client_id, settings.fief_client_secret)

oauth2 = OAuth2AuthorizationCodeBearer(
    f"{settings.fief_server_url}/authorize",
    f"{settings.fief_server_url}/api/token",
    scopes={"openid": "openid", "offline_access": "offline_access"},
    auto_error=False,
)

auth = FiefAuth(fief, oauth2)

AuthenticatedUser = Annotated[FiefAccessTokenInfo, Depends(auth.authenticated())]
