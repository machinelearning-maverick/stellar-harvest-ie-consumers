import asyncio
from aiokafka import AIOKafkaConsumer
from .config import settings
from .db.base import AsyncSessionLocal
from .db.models import KpIndexRecord
from .stream_parsers import parse_swpc


async def consume_topic(topic: str, parser, model_cls):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=[settings.KAFKA_URI],
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
        consume_topic(settings.KAFKA_SWPC_TOPIC, parse_swpc, KpIndexRecord)
    )


if __name__ == "__main__":
    asyncio.run(main())
