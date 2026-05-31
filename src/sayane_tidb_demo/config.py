from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


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
        if not self.tidb_host:
            raise ValueError("TIDB_HOST is required")
        return (
            f"mysql+pymysql://{self.tidb_user}:{self.tidb_password}"
            f"@{self.tidb_host}:{self.tidb_port}/{self.tidb_database}"
        )


def load_settings() -> Settings:
    return Settings()
