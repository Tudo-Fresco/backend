from http import HTTPStatus
from api.controllers.models.store.store_request_model import StoreRequestModel
from api.controllers.models.store.store_response_model import StoreResponseModel
from api.domain.entities.store import Store
from api.infrastructure.repositories.address_repository import AddressRepository
from api.infrastructure.repositories.store_repository import StoreRepository
from api.infrastructure.repositories.user_repository import UserRepository
from api.services.base_service import BaseService
from api.services.service_response import ServiceResponse


class StoreService(BaseService[StoreRequestModel, StoreResponseModel, Store]):
    def __init__(
        self,
        store_repository: StoreRepository,
        user_repository: UserRepository,
        address_repository: AddressRepository
    ):
        super().__init__(store_repository, Store, StoreResponseModel)
        self.user_repo = user_repository
        self.address_repo = address_repository

    async def create(self, request: StoreRequestModel) -> ServiceResponse[StoreResponseModel]:
        self.logger.log_info('Creating a Store')
        owner = await self.user_repo.get(request.owner_uuid)
        self._raise_not_found_when_none(owner, request.owner_uuid)
        address = await self.address_repo.get(request.address_uuid)
        self._raise_not_found_when_none(address, request.address_uuid)
        store = Store(
            cnpj=request.cnpj,
            trade_name=request.trade_name,
            legal_name=request.legal_name,
            legal_phone_contact=request.legal_phone_contact,
            preferred_phone_contact=request.preferred_phone_contact,
            legal_email_contact=request.legal_email_contact,
            preferred_email_contact=request.preferred_email_contact,
            images=request.images,
            reputation=request.reputation,
            owner=owner,
            address=address
        )
        created_id = await self.repository.create(store)
        response = StoreResponseModel(**store.to_dict())
        return ServiceResponse(
            status=HTTPStatus.CREATED,
            message=f'Loja {created_id} criada com sucesso',
            payload=response
        )