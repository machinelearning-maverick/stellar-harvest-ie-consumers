import asyncio
import pytest
from unittest.mock import Mock, AsyncMock, call

from stellar_harvest_ie_config.logging_config import setup_logging

setup_logging()

import stellar_harvest_ie_consumers.consumer as consumer_mod
from stellar_harvest_ie_consumers.consumer import consume_topic


class FakeMsg:
    def __init__(self, value):
        self.value = value


class DummyCM:
    def __init__(self, session):
        self._session = session

    async def __aenter__(self):
        return self._session

    async def __aexit__(self, exc_type, exc, tb):
        pass


@pytest.mark.asyncio
async def test_consume_topic_parsees_and_commits(monkeypatch):
    sample = {
        "time_tag": "2025-05-17T12:16:00",
        "kp_index": 1,
        "estimated_kp": 1.33,
        "kp": "1P",
    }

    async def infinite_msgs():
        yield FakeMsg(sample)
        yield FakeMsg(sample)
        while True:
            await asyncio.sleep(1)

    fake_consumer = AsyncMock()
    fake_consumer.__aiter__.side_effect = infinite_msgs

    monkeypatch.setattr(
        consumer_mod, "AIOKafkaConsumer", lambda *args, **kwargs: fake_consumer
    )
    monkeypatch.setattr(consumer_mod, "parse_planetary_kp_index", lambda v: v)

    class DummyService:
        def __init__(self, session):
            self.session = session

        async def create(self, data: dict):
            obj = object()
            self.session.add(obj)
            await self.session.commit()

    fake_session = Mock()
    fake_session.add = Mock()
    fake_session.commit = AsyncMock()

    monkeypatch.setattr(
        consumer_mod, "AsyncSessionLocal", lambda: DummyCM(fake_session)
    )

    task = asyncio.create_task(
        consume_topic(
            topic="dummy-topic",
            parser_func=consumer_mod.parse_planetary_kp_index,
            consumer_service_cls=DummyService,
        )
    )

    await asyncio.sleep(0.2)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert fake_session.add.call_count == 2
    assert fake_session.commit.call_count == 2

    expected_calls = [call(object()), call(object())]
    assert len(fake_session.add.mock_calls) == 2
    assert len(fake_session.commit.mock_calls) == 2
