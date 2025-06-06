import json
import asyncio
from aiokafka import AIOKafkaConsumer

from .settings import settings
from .stream_parsers import parse_planetary_kp_index

from stellar_harvest_ie_store.db import AsyncSessionLocal
from stellar_harvest_ie_models.stellar.swpc.entities import KpIndexEntity

from stellar_harvest_ie_config.utils.log_decorators import log_io


@log_io()
async def consume_topic(topic: str, parser_func, consumer_service_cls):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=[settings.kafka_uri],
        group_id=f"{topic}-consumer",
        auto_offset_reset="eraliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    await consumer.start()
    try:
        async for msg in consumer:
            raw_json = msg.value
            parsed_data = parser_func(raw_json)

            async with AsyncSessionLocal() as session:
                service = consumer_service_cls(session)
                try:
                    await service.create(parsed_data)
                except Exception as e:
                    print(f"[ERROR] Could not save: {parsed_data}, reason: {e}")
    finally:
        await consumer.stop()


@log_io()
async def main():
    await asyncio.gather(
        consume_topic(
            settings.kafka_topic_swpc, parse_planetary_kp_index, KpIndexEntity
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
