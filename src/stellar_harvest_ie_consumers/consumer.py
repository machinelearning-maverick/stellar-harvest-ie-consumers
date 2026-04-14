import json
import asyncio
from aiokafka import AIOKafkaConsumer

from stellar_harvest_ie_config.logging_config import setup_logging

setup_logging()

from stellar_harvest_ie_config.utils.log_decorators import log_io

from stellar_harvest_ie_consumers.settings import settings
from stellar_harvest_ie_consumers.stellar.swpc.service.kp_index_service import (
    KpIndexConsumerService,
)

from stellar_harvest_ie_store.db import AsyncSessionLocal


@log_io()
async def consume_topic(topic: str, consumer_service_cls):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=[settings.kafka_uri],
        group_id=f"{topic}-consumer",
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    await consumer.start()
    try:
        async for msg in consumer:
            async with AsyncSessionLocal() as session:
                service = consumer_service_cls(session)
                try:
                    await service.create(msg.value)
                except Exception as e:
                    print(f"[ERROR] Could not save: {msg.value}, reason: {e}")
    finally:
        await consumer.stop()


@log_io()
async def main():
    await asyncio.gather(consume_topic(settings.swpc_topic, KpIndexConsumerService))


if __name__ == "__main__":
    asyncio.run(main())
