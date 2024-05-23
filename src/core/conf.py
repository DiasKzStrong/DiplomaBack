from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="/Users/diasziada/Desktop/My Projects/DiplomaBack/diplomaback/.env",
        extra="ignore",
    )

    POSTGRES_URL: str


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
