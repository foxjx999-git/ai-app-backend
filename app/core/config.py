from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    app_name: str = " App Backend"
    app_version: str = "0.0.0"

    model_name: str = "gpt-4.0-mini"
    openai_api_key: str | None = None

    learning_log_file: str = "learning_log.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@lru_cache
def get_settings() ->Settings:
    return Settings()