from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfigError(Exception):
    """Raised when required TiDB connection settings are missing."""


class Settings(BaseSettings):
    tidb_host: str = ""
    tidb_port: int = 4000
    tidb_user: str = ""
    tidb_password: str = ""
    tidb_database: str = "sayane_context_demo"
    tidb_ssl_ca: str = ""

    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def sqlalchemy_url(self) -> str:
        validate_tidb_settings(self)
        return (
            f"mysql+pymysql://{self.tidb_user}:{self.tidb_password}"
            f"@{self.tidb_host}:{self.tidb_port}/{self.tidb_database}"
        )


def load_settings() -> Settings:
    return Settings()


def validate_tidb_settings(settings: Settings | None = None) -> Settings:
    resolved = settings or load_settings()
    missing = [
        name
        for name, value in (
            ("TIDB_HOST", resolved.tidb_host),
            ("TIDB_USER", resolved.tidb_user),
            ("TIDB_PASSWORD", resolved.tidb_password),
        )
        if not value
    ]
    if missing:
        fields = ", ".join(missing)
        raise DatabaseConfigError(
            "TiDB connection is not configured.\n"
            f"Missing required environment variable(s): {fields}\n"
            "Copy .env.example to .env and set your TiDB Cloud credentials:\n"
            "  cp .env.example .env"
        )
    return resolved
