from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False  # 기본값 설정

    class Config:
        env_file = ".env"  # 환경 변수 파일 경로 지정


settings = Settings()
