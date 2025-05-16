from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KAFKA_URI: str
    KAFKA_SWPC_TOPIC: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
