import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Audit Service"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    NOTIFY_WEBHOOK_URL: str | None = None
    
    # Database settings placeholder
    DATABASE_URL: str = "sqlite:///./audit.db"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
