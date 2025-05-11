from typing import List
from uuid import UUID
from api.exceptions.validation_exception import ValidationException
from api.infrastructure.repositories.demand_repository import DemandRepository
from api.infrastructure.repositories.product_repository import ProductRepository
from api.infrastructure.repositories.store_repository import StoreRepository
from api.infrastructure.repositories.user_repository import UserRepository
from api.controllers.models.demand.demand_response_mode import DemandResponseModel
from http import HTTPStatus
from api.controllers.models.demand.demand_request_model import DemandRequestModel
from api.domain.entities.demand import Demand
from api.services.base_service import BaseService
from api.services.service_exception_catcher import ServiceExceptionCatcher
from api.services.service_response import ServiceResponse


class DemandService(BaseService[DemandRequestModel, DemandResponseModel, Demand]):
    
    catch = ServiceExceptionCatcher('DemandExceptionCatcher')

    def __init__(
        self,
        demand_repository: DemandRepository,
        store_repository: StoreRepository,
        product_repository: ProductRepository,
        user_repository: UserRepository
    ):
        super().__init__(demand_repository, Demand, DemandResponseModel)
        self.store_repo = store_repository
        self.product_repo = product_repository
        self.user_repo = user_repository

    async def create(self, request: DemandRequestModel) -> ServiceResponse[DemandResponseModel]:
        self.logger.log_info('Creating a Demand')
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
        )
        created_id = await self.repository.create(demand)
        response = DemandResponseModel(**demand.to_dict())
        return ServiceResponse(
            status=HTTPStatus.CREATED,
            message=f'Demanda {created_id} criada com sucesso',
            payload=response
        )
    
    @catch
    async def list_by_store(self, user_uuid: UUID, store_uuid: UUID, page: int = 1, per_page: int = 10) -> ServiceResponse[List[DemandResponseModel]]:
        stores = await self.store_repo.list_by_owner(user_uuid)
        found_store = None 
        for store in stores:
            if str(store.owner.uuid) == str(user_uuid) and str(store.uuid) == str(store_uuid):
                found_store = store
                break
        if not found_store:
            raise ValidationException('O usuário não possui acesso a loja requerida')
        demands: List[Demand] = []
        demands = await self.repository.list_by_store(store_uuid, page, per_page)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'{len(demands)} demandas foram encontrados relacionados à loja {store_uuid}',
            payload=self._convert_many_to_response(demands)
        )