import asyncio
from aiokafka import AIOKafkaConsumer
from .settings import settings
from .db.bootstrap_db import AsyncSessionLocal
from stellar_harvest_ie_models.stellar.swpc.entities import KpIndexEntity
from .stream_parsers import parse_planetary_kp_index


async def consume_topic(topic: str, parser, model_cls):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=[settings.kafka_uri],
        group_id=f"{topic}-consumer",
        auto_offset_reset="eraliest",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = parser(msg.value)
            async with AsyncSessionLocal() as session:
                obj = model_cls(**data)
                session.add(obj)
                await session.commit()
    finally:
        await consumer.stop()


async def main():
    await asyncio.gather(
        consume_topic(
            settings.kafka_swpc_topic, parse_planetary_kp_index, KpIndexEntity
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
