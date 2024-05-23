from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import cache


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="/Users/diasziada/Desktop/My Projects/DiplomaBack/diplomaback/.env",
        extra="ignore",
    )

    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


@cache
def get_auth_settings() -> AuthSettings:
    return AuthSettings()


auth_settings = get_auth_settings()
