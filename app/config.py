import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Log Analytics Platform"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "lap")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "lap")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "lap")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    # If APP_ENV is testing and DATABASE_URL not provided, use local SQLite for simplicity
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./test.db" if os.getenv("APP_ENV") == "testing" else "postgresql+psycopg2://lap:lap@db:5432/lap",
    )

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

    KAFKA_BROKER: str = os.getenv("KAFKA_BROKER", "kafka:9092")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "logs")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
