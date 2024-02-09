from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    fief_server_url: str
    fief_client_id: str
    fief_client_secret: str

    class Config:
        env_file = "../config/.env"
        extra = "ignore" #'ignore' means: You have not to parametrize each field from the .env file - just parametrize these ones you need here like fief_server_url, fief_client_id etc.

settings = Settings()
