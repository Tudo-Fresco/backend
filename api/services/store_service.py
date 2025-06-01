from http import HTTPStatus
from typing import List
from uuid import UUID
from api.clients.receita_client import ReceitaClient
from api.controllers.models.store.store_request_model import StoreRequestModel
from api.controllers.models.store.store_response_model import StoreResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.domain.entities.store import Store
from api.enums.user_access import UserAccess
from api.exceptions.validation_exception import ValidationException
from api.infrastructure.repositories.address_repository import AddressRepository
from api.infrastructure.repositories.store_repository import StoreRepository
from api.infrastructure.repositories.user_repository import UserRepository
from api.services.base_service import BaseService
from api.services.service_exception_catcher import ServiceExceptionCatcher
from api.services.service_response import ServiceResponse


class StoreService(BaseService[StoreRequestModel, StoreResponseModel, Store]):

    catch = ServiceExceptionCatcher('StoreServiceExceptionCatcher')

    def __init__(
        self,
        store_repository: StoreRepository,
        user_repository: UserRepository,
        address_repository: AddressRepository
    ):
        super().__init__(store_repository, Store, StoreResponseModel)
        self.user_repo = user_repository
        self.address_repo = address_repository
    
    @catch
    async def create(self, request: StoreRequestModel) -> ServiceResponse[StoreResponseModel]:
        self.logger.log_info('Creating a Store')
        owner = await self.user_repo.get(request.owner_uuid)
        self._raise_not_found_when_none(owner, request.owner_uuid)
        address = await self.address_repo.get(request.address_uuid)
        self._raise_not_found_when_none(address, request.address_uuid)
        store = Store(
            cnpj=request.cnpj,
            address=address,
            reputation=0,
            trade_name=request.trade_name,
            legal_name=request.legal_name,
            owner=owner,
            legal_phone_contact=request.legal_phone_contact,
            preferred_phone_contact=request.preferred_phone_contact,
            legal_email_contact=request.legal_email_contact,
            preferred_email_contact=request.preferred_email_contact,
            store_type=request.store_type,
            opening_date=request.opening_date,
            size=request.size,
            legal_nature=request.legal_nature,
            cnae_code=request.cnae_code,
            branch_classification=request.branch_classification
        )
        created_id = await self.repository.create(store)
        response = StoreResponseModel(**store.to_dict())
        return ServiceResponse(
            status=HTTPStatus.CREATED,
            message=f'Loja {created_id} criada com sucesso',
            payload=response
        )
    
    @catch
    async def list_by_user(self, user_uuid: UUID, page: int = 1, per_page: int = 10) -> ServiceResponse[List[StoreResponseModel]]:
        user = await self.user_repo.get(user_uuid)
        stores: List[Store] = []
        if user.user_access == UserAccess.ADMIN or user.user_access == UserAccess.STORE_OWNER:
            stores = await self.repository.list_by_owner(user_uuid, page, per_page)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'{len(stores)} pontos de venda foram encontrados relacionados ao usuário {user_uuid}',
            payload=self._convert_many_to_response(stores)
        )
    
    @catch
    async def fresh_fill(self, cnpj: str) -> ServiceResponse[StoreResponseModel]:
        receita_client = ReceitaClient()
        partially_filled_store_response_model = await receita_client.get_by_cnpj(cnpj)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'A empresa {partially_filled_store_response_model.legal_name}, Cnpj: {cnpj} foi encontrada com sucesso na Receita Federal',
            payload=partially_filled_store_response_model
        )
    
    @catch
    async def update(self, obj_id: UUID, request: StoreRequestModel, user: UserResponseModel) -> ServiceResponse[StoreResponseModel]:
        store = await self.repository.get(obj_id)
        if not (user.user_access == UserAccess.ADMIN or user.uuid == store.owner):
            raise ValidationException(f'O usuário {user.email} não possui o privilégio necessário para alterar os dados uma empresa')
        store.update(**request.model_dump())
        store.validate()
        await self.repository.update(store)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'A empresa {store.legal_name} foi atualizada com sucesso',
            payload=StoreResponseModel(store.to_dict())
        )
    
    @catch
    async def delete(self, obj_id: UUID, user: UserResponseModel) -> ServiceResponse[None]:
        store = await self.repository.get(obj_id)
        if not (user.user_access == UserAccess.ADMIN or user.uuid == store.owner):
            raise ValidationException(f'O usuário {user.email} não possui o privilégio necessário para excluir uma empresa')
        store.deactivate()
        await self.repository.update(store)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'A empresa {store.legal_name} foi excluída com sucesso'
        )