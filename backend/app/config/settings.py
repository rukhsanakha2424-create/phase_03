import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    undo_token_secret: str = Field(..., alias="UNDO_TOKEN_SECRET")
    request_id_header: str = Field("X-Request-ID", alias="REQUEST_ID_HEADER")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    class Config:
        env_file = str(BASE_DIR / ".env")  # Points to backend/.env
        env_file_encoding = "utf-8"
        extra = "ignore"

def get_settings() -> Settings:
    return Settings()

settings = get_settings()
print("USING DATABASE:", settings.database_url)
