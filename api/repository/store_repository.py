from api.infrastructure.models.store_model import StoreModel
from api.repository.base_repository import BaseRepository


class StoreRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session, StoreModel)