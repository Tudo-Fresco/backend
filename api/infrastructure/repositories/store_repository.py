from api.infrastructure.models.store_model import StoreModel
from api.infrastructure.repositories import base_repository
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.entities.store import Store


class StoreRepository(base_repository[Store, StoreModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, StoreModel)