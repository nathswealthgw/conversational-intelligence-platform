from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Conversational Intelligence Platform"
    version: str = "0.1.0"
    environment: str = "local"
    log_level: str = "INFO"
    cors_origins: List[str] = ["*"]

    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"
    faiss_index_path: str = "./data/faiss.index"
    document_store_path: str = "./data/documents.jsonl"

    jwt_secret: str = Field("change-me", env="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    postgres_dsn: str = Field("sqlite:///./app.db", env="POSTGRES_DSN")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")

    class Config:
        env_file = ".env"
        case_sensitive = False

    def validate_runtime(self) -> None:
        if self.environment == "production" and not self.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required in production")


@lru_cache
def get_settings() -> Settings:
    return Settings()
