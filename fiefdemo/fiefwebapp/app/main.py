####################################

# Imports

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from auth import AuthenticatedUser, auth, fief
from config.settings import settings

####################################

# App

app = FastAPI()

####################################

# Example endpoint which is using authentification (auth.py)
#@app.get("/user")
#async def read_users_me(user: AuthenticatedUser = Depends(auth.authenticated())):
#    return {"user": user}

####################################

# Example endpoints which are using manual authentification

# Start Authentificationprocess
@app.get("/auth/login")
async def login():
    redirect_url = "http://fief.mydomain.com/docs/oauth2-redirect"
    auth_url = await fief.auth_url(redirect_url, scope=["openid"])
    return RedirectResponse(url=auth_url)

# Callback-Endpoint, which is called after the Authentificationprocess
@app.get("/auth/callback")
async def auth_callback(code: str):
    redirect_url = "http://fief.mydomain.com/docs/oauth2-redirect"
    try:
        tokens, userinfo = await fief.auth_callback(code, redirect_url)
        # Implement your logic
        print(f"Tokens: {tokens}")
        print(f"Userinfo: {userinfo}")
        return {"tokens": tokens, "userinfo": userinfo}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

####################################
