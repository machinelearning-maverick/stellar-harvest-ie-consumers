import logging
from stellar_harvest_ie_config.logging_config import setup_logging

setup_logging()

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

KAFKA_URI = "KAFKA_URI"
KAFKA_TOPIC_SWPC = "KAFKA_TOPIC_SWPC"


class ConsumerSettings(BaseSettings):
    logger.info("ConsumerSettings()")

    model_config = SettingsConfigDict(env_file=None)

    kafka_uri: str = Field("kafka:9092", env=KAFKA_URI)
    swpc_topic: str = Field(
        "stellar-harvest-ie-raw-space-weather", env=KAFKA_TOPIC_SWPC
    )
    database_url: str = Field("postgresql+asyncpg://app:secret@postgres/ui_db")

    # class Config:
    #     env_file = ".env"


settings = ConsumerSettings()
