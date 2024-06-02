from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False  # 기본값 설정

    sentry_enable: bool = False
    sentry_dsn: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
