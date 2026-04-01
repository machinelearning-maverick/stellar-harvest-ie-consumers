from typing import Dict
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from stellar_harvest_ie_store.repository import AsyncRepository
from stellar_harvest_ie_models.stellar.swpc.entities import KpIndexEntity
from stellar_harvest_ie_consumers.service.kp_index_parser import KpIndexConsumerParser

from stellar_harvest_ie_config.utils.log_decorators import log_io


class KpIndexConsumerService:
    def __init__(self, session: AsyncSession):
        self.repository = AsyncRepository(KpIndexEntity, session)

    @log_io()
    async def create(self, data: Dict) -> KpIndexEntity:
        entity = KpIndexEntity(entity=KpIndexConsumerParser.parse(data))

        saved = await self.repository.add(entity)
        return saved
