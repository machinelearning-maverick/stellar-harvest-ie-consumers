import logging

from stellar_harvest_ie_config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConsumerSettings(BaseSettings):
    logger.info("ConsumerSettings()")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    kafka_uri: str
    kafka_topic_swpc: str


settings = ConsumerSettings()
