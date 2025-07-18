from typing import List
from uuid import UUID
from fastapi import Body, Depends, Query
from fastapi.responses import JSONResponse
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.store.store_request_model import StoreRequestModel
from api.controllers.models.store.store_response_model import StoreResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.enums.user_access import UserAccess
from api.controllers.base_controller import BaseController
from api.services.service_response import ServiceResponse
from api.services.store_service import StoreService


class StoreController(BaseController[StoreRequestModel, StoreResponseModel]):

    def __init__(self, service: StoreService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=StoreRequestModel,
            response_model=StoreResponseModel,
            prefix="/store",
            tag=__class__.__name__,
            auth_wrapper=auth_wrapper
        )
        self.router.add_api_route(
            path='/list-by-user',
            endpoint=self._list_by_user_handler(),
            methods=['GET'],
            response_model=List[StoreResponseModel],
            status_code=200,
            summary=f'Listing {self.__class__.__name__} by owner'
        )
        self.router.add_api_route(
            path='/fresh-fill',
            endpoint=self._fresh_fill_handler(),
            methods=['GET'],
            response_model=StoreResponseModel,
            status_code=200,
            summary='Fetch partially filled company data by CNPJ'
        )

    def _create_handler(self):
        async def create(
                model: StoreRequestModel = Body(...), 
                user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))
            ) -> JSONResponse:
            self.logger.log_info("Creating a new store")
            if not model.owner_uuid:
                 model.owner_uuid = user.uuid
                 self.logger.log_info(f'The owner uuid was not informed for this store, assuming the owner is the caller {user.uuid}')
            service_response: ServiceResponse = await self.service.create(request=model)
            return self.make_response(service_response)
        return create

    def _list_by_user_handler(self):
            async def list_by_user(
                page: int = Query(...), per_page: int = Query(10),
                user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))
            ) -> JSONResponse:
                self.logger.log_info(f'Listing the stores for the user {user.uuid}, page: {page}, per page: {per_page}')
                service_response: ServiceResponse = await self.service.list_by_user(
                    user_uuid=user.uuid,
                    page=page,
                    per_page=per_page
                )
                return self.make_response(service_response)
            return list_by_user
    
    def _fresh_fill_handler(self):
        async def fresh_fill(
            cnpj: str = Query(..., description="CNPJ of the company to fetch")
        ) -> JSONResponse:
            service_response: ServiceResponse = await self.service.fresh_fill(cnpj=cnpj)
            return self.make_response(service_response)
        return fresh_fill
    
    def _update_handler(self):
        async def update(
                uuid: UUID,
                model: StoreRequestModel = Body(...),
                user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))) -> JSONResponse:
            self.logger.log_info(f"Updating store {uuid}")
            service_response: ServiceResponse = await self.service.update(obj_id=uuid, request=model, user=user)
            return self.make_response(service_response)
        return update
    
    def _delete_handler(self):
        async def delete(
                uuid: UUID,
                user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.STORE_OWNER, UserAccess.ADMIN]))) -> JSONResponse:
            self.logger.log_info(f"Updating store {uuid}")
            service_response: ServiceResponse = await self.service.delete(obj_id=uuid, user=user)
            return self.make_response(service_response)
        return delete