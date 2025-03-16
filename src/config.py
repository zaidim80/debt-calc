from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="debt_",
        env_file_encoding="utf-8",
    )
    host: str = Field("localhost")
    port: int = Field(8000)
    dsn: str = Field("postgresql+asyncpg://postgres:postgres@db:5432/postgres", alias="DSN")
    redis: str = Field("localhost")

    auth_secret: str = Field("mega-secret")

    test_url: str = Field("http://localhost:8000/")


cfg = Settings()
