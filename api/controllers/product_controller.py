from typing import List
from uuid import UUID
from fastapi.responses import JSONResponse
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.product.product_request_model import ProductRequestModel
from api.controllers.models.product.product_response_model import ProductResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.enums.product_type import ProductType
from api.enums.user_access import UserAccess
from api.services.i_service import IService
from fastapi import Depends, File, Query, UploadFile
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
        self.router.add_api_route(
            path='/product-picture',
            endpoint=self._upload_picture_handler(),
            methods=['POST'],
            response_model=UserResponseModel,
            status_code=200,
            summary=f'Upload a picture for {self.__class__.__name__}'
        )
        self.router.add_api_route(
            path='/product-picture',
            endpoint=self._delete_picture_handler(),
            methods=['DELETE'],
            response_model=UserResponseModel,
            status_code=200,
            summary=f'Delete a picture for {self.__class__.__name__}'
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
    
    def _upload_picture_handler(self):
        async def upload_picture(
            file: UploadFile = File(...),
            product_uuid: UUID = Query(...),
            user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))
        ) -> JSONResponse:
            self.logger.log_info(f'New profile picture being uploaded from the user {user.uuid} for the product {product_uuid}')
            image_bytes = await file.read()
            file_name = file.filename
            service_response: ServiceResponse = await self.service.upload_picture(
                product_uuid=product_uuid,
                image_bytes=image_bytes,
                file_name=file_name
            )
            return self.make_response(service_response)
        return upload_picture
    
    def _delete_picture_handler(self):
        async def delete_picture(
            product_uuid: UUID = Query(),
            picture_index: int = Query(),
            user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))
        ) -> JSONResponse:
            self.logger.log_info(f'Deleting the picture {picture_index} on the product {product_uuid} from the user {user.uuid}')
            service_response: ServiceResponse = await self.service.delete_picture(
                product_uuid=product_uuid,
                image_index=picture_index
            )
            return self.make_response(service_response)
        return delete_picture