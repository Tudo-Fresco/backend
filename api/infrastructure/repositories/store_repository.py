from typing import List
from uuid import UUID
from api.infrastructure.models.store_model import StoreModel
from api.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.entities.store import Store
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


class StoreRepository(BaseRepository[Store, StoreModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, StoreModel)

    async def list_by_owner(self, owner_uuid: UUID, page: int = 1, per_page: int = 10) -> List[Store]:
            self.logger.log_debug(f'Listing companies by the owner: {owner_uuid} (page {page}, per_page {per_page})')
            if page < 1:
                page = 1
            query = (
                select(self.model_class)
                .filter_by(active=True)
                .filter(self.model_class.owner_uuid == owner_uuid)
                .options(
                    joinedload(StoreModel.address),
                    joinedload(StoreModel.owner)
                )
                .offset((page - 1) * per_page)
                .limit(per_page)
            )
            result = await self.session.execute(query)
            models = result.scalars().all()
            stores: List[Store] = []
            for model in models:
                store: Store = model.to_entity()
                stores.append(store)
            return stores
