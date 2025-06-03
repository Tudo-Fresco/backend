from typing import List
from uuid import UUID
from fastapi import Body, Depends, Query
from fastapi.responses import JSONResponse
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.demand.demand_request_model import DemandRequestModel
from api.controllers.models.demand.demand_response_mode import DemandResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.enums.demand_status import DemandStatus
from api.enums.product_type import ProductType
from api.enums.user_access import UserAccess
from api.services.demand_service import DemandService
from api.services.i_service import IService
from api.controllers.base_controller import BaseController
from api.services.service_response import ServiceResponse


class DemandController(BaseController[DemandRequestModel, DemandResponseModel]):

    def __init__(self, service: DemandService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=DemandRequestModel,
            response_model=DemandResponseModel,
            prefix="/demand",
            tag=__class__.__name__,
            auth_wrapper=auth_wrapper
        )
        self.router.add_api_route(
            path='/list-by-store',
            endpoint=self._list_by_store_handler(),
            methods=['GET'],
            response_model=List[DemandResponseModel],
            status_code=200,
            summary=f'Listing {self.__class__.__name__} by store'
        )
    
    def _create_handler(self):
        async def create(model: DemandRequestModel = Body(...),
                        user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))) -> JSONResponse:
            self.logger.log_info('Creating a new demand')
            service_response: ServiceResponse = await self.service.create(user=user, request=model)
            return self.make_response(service_response)
        return create

    def _list_by_store_handler(self):
            async def list_by_store(
                store_uuid: UUID, page: int = Query(1), per_page: int = Query(10), radius_meters: int = 10000, product_type: ProductType = ProductType.ANY,
                status: DemandStatus = DemandStatus.ANY,
                user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))
            ) -> JSONResponse:
                self.logger.log_info(f'Listing the demands for the store {store_uuid}, page: {page}, per page: {per_page}')
                service_response: ServiceResponse = await self.service.list_by_store(
                    user=user,
                    store_uuid=store_uuid,
                    status=status,
                    page=page,
                    per_page=per_page,
                    radius_meters=radius_meters,
                    product_type=product_type
                )
                return self.make_response(service_response)
            return list_by_store