from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Supply Chain Management API"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./supply_chain.db")
    
    # CORS - we'll handle this completely outside of pydantic
    
    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore"  # This tells pydantic to ignore extra fields from env vars
    }
    
    def model_post_init(self, __context):
        # Check for SECRET_KEY after initialization
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable is not set")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# Define ALLOWED_ORIGINS outside of the Settings class
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
