from typing import List
from uuid import UUID
from api.domain.entities.demand import Demand
from api.infrastructure.models.demand_model import DemandModel
from api.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select


class DemandRepository(BaseRepository[Demand, DemandModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DemandModel)

    async def list_by_store(self, store_uuid: UUID, page: int = 1, per_page: int = 10) -> List[Demand]:
        self.logger.log_debug(f'Listing demands by the store: {store_uuid} (page {page}, per_page {per_page})')
        if page < 1:
            page = 1
        query = (
            select(self.model_class)
            .filter_by(active=True)
            .filter(self.model_class.store_uuid == store_uuid)
            .options(
                joinedload(DemandModel.store),
                joinedload(DemandModel.product)
            )
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        stores: List[Demand] = []
        for model in models:
            store: Demand = model.to_entity()
            stores.append(store)
        return stores