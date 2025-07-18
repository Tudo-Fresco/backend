from typing import List
from uuid import UUID
from api.controllers.models.user.user_response_model import UserResponseModel
from api.enums.demand_status import DemandStatus
from api.enums.product_type import ProductType
from api.exceptions.unauthorized_exception import UnauthorizedException
from api.infrastructure.repositories.demand_repository import DemandRepository
from api.infrastructure.repositories.product_repository import ProductRepository
from api.infrastructure.repositories.store_repository import StoreRepository
from api.infrastructure.repositories.user_repository import UserRepository
from api.controllers.models.demand.demand_response_model import DemandResponseModel
from http import HTTPStatus
from api.controllers.models.demand.demand_request_model import DemandRequestModel
from api.domain.entities.demand import Demand
from api.services.base_service import BaseService
from api.services.product_service import ProductService
from api.services.service_exception_catcher import ServiceExceptionCatcher
from api.services.service_response import ServiceResponse


class DemandService(BaseService[DemandRequestModel, DemandResponseModel, Demand]):
    
    catch = ServiceExceptionCatcher('DemandExceptionCatcher')

    def __init__(
        self,
        demand_repository: DemandRepository,
        store_repository: StoreRepository,
        product_repository: ProductRepository,
        user_repository: UserRepository,
        product_service: ProductService
    ):
        super().__init__(demand_repository, Demand, DemandResponseModel)
        self.store_repo = store_repository
        self.product_repo = product_repository
        self.user_repo = user_repository
        self.product_service = product_service

    async def create(self, user: UserResponseModel, request: DemandRequestModel) -> ServiceResponse[DemandResponseModel]:
        self.logger.log_info('Creating a Demand')
        if not request.responsible_uuid:
            request.responsible_uuid = user.uuid
            self.logger.log_warning(f'No responsible user was informed for this demand, the responsible will be the creator {user.email}: {user.uuid}')
        await self._raise_if_user_is_not_authorized(user, request.store_uuid)
        store = await self.store_repo.get(request.store_uuid)
        self._raise_not_found_when_none(store, request.store_uuid)
        product = await self.product_repo.get(request.product_uuid)
        self._raise_not_found_when_none(product, request.product_uuid)
        responsible = await self.user_repo.get(request.responsible_uuid)
        self._raise_not_found_when_none(responsible, request.responsible_uuid)
        demand = Demand(
            store=store,
            product=product,
            responsible=responsible,
            needed_count=request.needed_count,
            description=request.description,
            deadline=request.deadline,
            status=DemandStatus.OPENED,
            minimum_count=request.minimum_count
        )
        created_id = await self.repository.create(demand)
        response = DemandResponseModel(**demand.to_dict())
        return ServiceResponse(
            status=HTTPStatus.CREATED,
            message=f'Demanda {created_id} criada com sucesso',
            payload=response
        )
    
    @catch
    async def get(self, obj_id: UUID, user: UserResponseModel, store_uuid: UUID) -> ServiceResponse[DemandResponseModel]:
        self.logger.log_info(f'Reading from id {obj_id}')
        await self._raise_if_user_is_not_authorized(user, store_uuid)
        demand = await self.repository.get(obj_id)
        await self.product_service.sign_product_images(demand.product)
        self._raise_not_found_when_none(demand, obj_id)
        response = DemandResponseModel(**demand.to_dict())
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'A demanda {obj_id} foi encontrada com sucesso',
            payload=response
            )

    @catch
    async def list_by_store(self, user: UserResponseModel,
                            store_uuid: UUID,
                            status: DemandStatus = DemandStatus.ANY,
                            page: int = 1,
                            per_page: int = 10,
                            radius_meters: int = 10000,
                            product_type: ProductType = ProductType.ANY
                            ) -> ServiceResponse[List[DemandResponseModel]]:
        await self._raise_if_user_is_not_authorized(user, store_uuid)
        self.logger.log_debug(f'Listing by the stauts {status.value}')
        demands: List[Demand] = []
        demands = await self.repository.list_by_store(store_uuid, status, page, per_page, radius_meters, product_type)
        for demand in demands:
            await self.product_service.sign_product_images(demand.product)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'{len(demands)} demandas com o status {status.value} foram encontrados para a loja selecionada',
            payload=self._convert_many_to_response(demands)
        )
    
    async def _raise_if_user_is_not_authorized(self, user: UserResponseModel, store_uuid: UUID) -> None:
        self.logger.log_debug(f'Cheking if the user {user.uuid} has access to the store {store_uuid}')
        stores = await self.store_repo.list_by_owner(user.uuid, 1, 1000000)
        found_store = None 
        for store in stores:
            if str(store.owner.uuid) == str(user.uuid) and str(store.uuid) == str(store_uuid):
                found_store = store
                break
        if not found_store:
            self.logger.log_warning(f'The user {user.uuid} does not have access to the store {store_uuid}')
            raise UnauthorizedException('O usuário não possui acesso a loja requerida')
        self.logger.log_debug(f'User {user.uuid} has access to the store {store_uuid}')