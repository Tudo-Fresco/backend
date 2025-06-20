from typing import List
from uuid import UUID
from fastapi.responses import JSONResponse
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.post.post_response_model import PostResponseModel
from api.controllers.models.product.product_request_model import ProductRequestModel
from api.controllers.models.product.product_response_model import ProductResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.enums.demand_status import DemandStatus
from api.enums.product_type import ProductType
from api.enums.user_access import UserAccess
from fastapi import Depends, Query
from api.controllers.base_controller import BaseController
from api.services.reel_service import ReelService
from api.services.service_response import ServiceResponse


class ReelController(BaseController[None, PostResponseModel]):

    def __init__(self, service: ReelService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=ProductRequestModel,
            response_model=ProductResponseModel,
            prefix="/reel",
            tag=__class__.__name__,
            auth_wrapper=auth_wrapper
        )
        self.router.add_api_route(
            path='/posts',
            endpoint=self._posts_handler(),
            methods=['GET'],
            response_model=List[ProductResponseModel],
            status_code=200,
            summary='Fetch posts considering the store coordinates and other query filters'
        )

    def _posts_handler(self):
            async def get_posts(
                store_uuid: UUID, page: int = Query(1),
                per_page: int = Query(10),
                radius_meters: int = 10000,
                product_type: ProductType = ProductType.ANY,
                status: DemandStatus = DemandStatus.ANY,
                user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))
            ) -> JSONResponse:
                self.logger.log_info(f'Listing the demands for the store {store_uuid}, page: {page}, per page: {per_page}')
                service_response: ServiceResponse = await self.service.get_posts(
                    user=user,
                    store_uuid=store_uuid,
                    status=status,
                    page=page,
                    per_page=per_page,
                    radius_meters=radius_meters,
                    product_type=product_type
                )
                return self.make_response(service_response)
            return get_posts