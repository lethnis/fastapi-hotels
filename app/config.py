from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_password: str
    postgres_user: str
    postgres_db: str
    postgres_hostname: str
    postgres_port: int
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


DATABASE_URL = (
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_hostname}:{settings.postgres_port}/{settings.postgres_db}"
)

ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_hostname}:{settings.postgres_port}/{settings.postgres_db}"
)
