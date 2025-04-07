from api.infrastructure.models.store_model import StoreModel
from api.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.entities.store import Store


class StoreRepository(BaseRepository[Store, StoreModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, StoreModel)