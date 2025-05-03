from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.address.address_request_model import AddressRequestModel
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.enums.user_access import UserAccess
from api.services.i_service import IService
from api.controllers.base_controller import BaseController
from api.services.service_response import ServiceResponse


class AddressController(BaseController[AddressRequestModel, AddressResponseModel]):

    def __init__(self, service: IService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=AddressRequestModel,
            response_model=AddressResponseModel,
            prefix="/address",
            tag=__class__.__name__,
            auth_wrapper=auth_wrapper
        )
        self.router.add_api_route(
            path='/fresh-fill',
            endpoint=self._fresh_fill_handler(),
            methods=['GET'],
            response_model=AddressResponseModel,
            status_code=200,
            summary='Fetch partially filled address data by CEP',
            dependencies=[Depends(self.auth_wrapper.with_access([UserAccess.ADMIN, UserAccess.STORE_OWNER]))]
        )

    def _fresh_fill_handler(self):
        async def fresh_fill(
            cep: str = Query(..., description="CEP of the address to fetch")
        ) -> JSONResponse:
            service_response: ServiceResponse = await self.service.fresh_fill(cep=cep)
            return self.make_response(service_response)
        return fresh_fill