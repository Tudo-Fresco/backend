from api.infrastructure.models.store_model import StoreModel
from api.domain.store import Store
from api.repository.base_repository import BaseRepository


class StoreRepository(BaseRepository[Store, StoreModel]):

    def __init__(self, db_session):
        super().__init__(db_session, Store, StoreModel)
