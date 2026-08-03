"""Application configuration loaded from environment variables.

Settings are read from the process environment and, if present, a local
``.env`` file. ``get_settings`` is cached so the configuration is parsed once
per process and injected wherever it is needed.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the application.

    Field values come from environment variables (case-insensitive). Unknown
    variables in the environment or ``.env`` file are ignored, so the file can
    document settings that later milestones will consume.
    """

    app_name: str = "Document Intelligence RAG Platform"
    app_env: str = "development"
    log_level: str = "INFO"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached ``Settings`` instance for dependency injection."""
    return Settings()
