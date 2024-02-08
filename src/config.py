from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='debt_',
        env_file_encoding='utf-8',
    )
    host: str = Field('localhost')
    port: int = Field(8000)
    project_name: str = Field('Калькулятор долгов')
    dsn: str = Field('postgresql+asyncpg://postgres:postgres@localhost:5432/postgres')

    test_url: str = Field('http://localhost:8000/')


cfg = Settings()
