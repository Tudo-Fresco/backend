from typing import List
from fastapi.responses import JSONResponse
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.product.product_request_model import ProductRequestModel
from api.controllers.models.product.product_response_model import ProductResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.enums.product_type import ProductType
from api.enums.user_access import UserAccess
from api.services.i_service import IService
from fastapi import Depends, Query
from api.controllers.base_controller import BaseController
from api.services.service_response import ServiceResponse


class ProductController(BaseController[ProductRequestModel, ProductResponseModel]):

    def __init__(self, service: IService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=ProductRequestModel,
            response_model=ProductResponseModel,
            prefix="/product",
            tag=__class__.__name__,
            auth_wrapper=auth_wrapper
        )
        self.router.add_api_route(
            path='/search',
            endpoint=self._search_handler(),
            methods=['GET'],
            response_model=List[ProductResponseModel],
            status_code=200,
            summary='Fetch products by name or type'
        )

    def _search_handler(self):
        async def search(
            name: str = Query('*'), type: ProductType = Query(ProductType.ANY),
            page: int = Query(1), per_page: int = Query(10),
            user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))
        ) -> JSONResponse:
            self.logger.log_info(f'Listing the stores for the user {user.uuid}, page: {page}, per page: {per_page}')
            service_response: ServiceResponse = await self.service.list_by_name_and_type(
                name=name,
                type=type,
                page=page,
                per_page=per_page
            )
            return self.make_response(service_response)
        return search