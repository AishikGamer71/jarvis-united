from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # LLM Provider Keys
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # DB & Infrastructure
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/jarvis"
    redis_url: str = "redis://localhost:6379/0"
    
    # Environment
    environment: str = "development"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
