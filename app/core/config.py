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

    docs_dir: str = "data/docs"
    rag_top_k: int = 3
    rag_retrieval_mode: str = "vector"

    embedding_model: str = "text-embedding-3-small"
    chroma_dir: str = "chroma_db"
    chroma_collection_name: str = "ai_app_docs" 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@lru_cache
def get_settings() ->Settings:
    return Settings()