from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "ai_sql_assistant.db"


class Settings(BaseSettings):
    app_name: str = "AI SQL Assistant"
    environment: str = "development"
    ai_provider: str = Field(default="gemini", alias="AI_PROVIDER")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    google_api_key: str | None = Field(default=None, alias="GOOGLE_API_KEY")
    gemini_model: str = Field(default="gemini-3.6-flash", alias="GEMINI_MODEL")
    database_url: str = Field(
        default=f"sqlite:///{DATABASE_PATH.as_posix()}",
        alias="DATABASE_URL",
    )
    allow_dangerous_sql: bool = Field(default=False, alias="ALLOW_DANGEROUS_SQL")
    frontend_origin: str = Field(default="http://localhost:5173", alias="FRONTEND_ORIGIN")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
