from typing import List
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.store.store_request_model import StoreRequestModel
from api.controllers.models.store.store_response_model import StoreResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.enums.user_access import UserAccess
from api.services.i_service import IService
from api.controllers.base_controller import BaseController
from api.services.service_response import ServiceResponse


class StoreController(BaseController[StoreRequestModel, StoreResponseModel]):

    def __init__(self, service: IService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=StoreRequestModel,
            response_model=StoreResponseModel,
            prefix="/store",
            tag=__class__.__name__,
            auth_wrapper=auth_wrapper
        )
        self.router.add_api_route(
            path='/list-by-owner',
            endpoint=self._list_by_owner_handler(),
            methods=['GET'],
            response_model=List[StoreResponseModel],
            status_code=200,
            summary=f'Listing {self.__class__.__name__} by owner',
            dependencies=[Depends(self.auth_wrapper.with_access([UserAccess.ADMIN, UserAccess.STORE_OWNER]))]
        )

    def _list_by_owner_handler(self):
            async def list_by_owner(
                page: int = Query(...), per_page: int = Query(10),
                user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))
            ) -> JSONResponse:
                self.logger.log_info(f'Listing the stores for the owner {user.uuid}, page: {page}, per page: {per_page}')
                service_response: ServiceResponse = await self.service.list_by_owner(
                    owner_uuid=user.uuid,
                    page=page,
                    per_page=per_page
                )
                return self.make_response(service_response)
            return list_by_owner