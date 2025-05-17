import asyncio
import pytest
from unittest.mock import AsyncMock

import stellar_harvest_ie_consumers.consumer as consumer_mod
from stellar_harvest_ie_consumers.consumer import consume_topic


class FakeMsg:
    def __init__(self, value):
        self.value = value


@pytest.mark.asyncio
async def test_consume_topic_parsees_and_commits(monkeypatch):
    sample = {
        "time_tag": "2025-05-17T12:16:00",
        "kp_index": 1,
        "estimated_kp": 1.33,
        "kp": "1P",
    }

    fake_consumer = AsyncMock()
    fake_consumer.__aiter__.return_value = [FakeMsg(sample), FakeMsg(sample)]

    pass
