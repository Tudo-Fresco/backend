from api.controllers.models.store.store_request_model import StoreRequestModel
from api.controllers.models.store.store_response_model import StoreResponseModel
from api.domain.entities.store import Store
from api.infrastructure.repositories.store_repository import StoreRepository
from api.services.base_service import BaseService


class StoreService(BaseService[StoreRequestModel, StoreResponseModel, Store]):
    def __init__(self, store_repository: StoreRepository):
        super().__init__(store_repository, Store)