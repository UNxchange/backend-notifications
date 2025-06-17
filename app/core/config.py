# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()
