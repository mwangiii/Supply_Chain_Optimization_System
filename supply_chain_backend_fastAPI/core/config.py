from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List
from functools import lru_cache

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Supply Chain Management API"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "4f8b31dc8ee3437486e3424bcb2d6f0b"  # Should be in environment variables in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./supply_chain.db"
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()