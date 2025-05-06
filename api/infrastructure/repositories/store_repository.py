from typing import List, Optional
from uuid import UUID
from api.exceptions.not_found_exception import NotFoundException
from api.infrastructure.models.store_model import StoreModel
from api.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.entities.store import Store
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


class StoreRepository(BaseRepository[Store, StoreModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, StoreModel)

    async def get(self, obj_id: UUID) -> Store:
        self.logger.log_debug(f'Retrieving store: {obj_id}')
        query = (
            select(self.model_class)
            .filter_by(uuid=obj_id, active=True)
            .options(
                joinedload(StoreModel.address),
                joinedload(StoreModel.owner)
            )
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            self.logger.log_warning(f'No active store found for UUID: {obj_id}')
            raise NotFoundException(f'Nenhuma loja com o id {obj_id} foi encontrada')
        return model.to_entity()

    async def list(self, page: int = 1, per_page: int = 10) -> List[Store]:
        self.logger.log_debug(f'Listing stores (page {page}, per_page {per_page})')
        if page < 1:
            page = 1
        query = (
            select(self.model_class)
            .filter_by(active=True)
            .options(
                joinedload(StoreModel.address),
                joinedload(StoreModel.owner)
            )
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [model.to_entity() for model in models]

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

    async def get_by_cnpj(self, cnpj: str) -> Optional[Store]:
        self.logger.log_debug(f'Fetching store by CNPJ: {cnpj}')
        query = (
            select(self.model_class)
            .filter_by(active=True)
            .filter(self.model_class.cnpj == cnpj)
            .options(
                joinedload(StoreModel.address),
                joinedload(StoreModel.owner)
            )
        )
        result = await self.session.execute(query)
        model = result.scalars().first()
        if model:
            return model.to_entity()
        return None