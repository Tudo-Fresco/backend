from typing import Any, Generic, TypeVar, Type, List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import JSONResponse
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.base_request_model import BaseRequestModel
from api.controllers.models.base_response_model import BaseResponseModel
from api.enums.user_access import UserAccess
from api.services.i_service import IService
from api.services.service_response import ServiceResponse
from api.shared.logger import Logger
from fastapi.encoders import jsonable_encoder

RequestModelT = TypeVar('RequestModelT', bound=BaseRequestModel)
ResponseModelT = TypeVar('ResponseModelT', bound=BaseResponseModel)

class BaseController(Generic[RequestModelT, ResponseModelT]):
    def __init__(
        self,
        service: IService,
        request_model: Type[RequestModelT],
        response_model: Type[ResponseModelT],
        prefix: str,
        tag: str,
        auth_wrapper: AuthWrapper
    ):
        self.service = service
        self.logger = Logger(tag)
        self.router = APIRouter(prefix=prefix, tags=[tag])
        self.request_model = request_model
        self.response_model = response_model
        self.auth_wrapper = auth_wrapper

        self.router.add_api_route(
            path="/",
            endpoint=self._create_handler(),
            methods=["POST"],
            response_model=response_model,
            status_code=201,
            summary=f"Create {tag}",
            dependencies=[Depends(self.auth_wrapper.with_access([UserAccess.ADMIN]))]
        )
        self.router.add_api_route(
            path="/{uuid}",
            endpoint=self._get_handler(),
            methods=["GET"],
            response_model=response_model,
            summary=f"Get {tag} by UUID",
            dependencies=[Depends(self.auth_wrapper.with_access([UserAccess.ADMIN]))]
        )
        self.router.add_api_route(
            path="/",
            endpoint=self._list_handler(),
            methods=["GET"],
            response_model=List[response_model],
            summary=f"List {tag}s",
            dependencies=[Depends(self.auth_wrapper.with_access([UserAccess.ADMIN]))]
        )
        self.router.add_api_route(
            path="/{uuid}",
            endpoint=self._update_handler(),
            methods=["PUT"],
            response_model=response_model,
            summary=f"Update {tag} by UUID",
            dependencies=[Depends(self.auth_wrapper.with_access([UserAccess.ADMIN]))]
        )
        self.router.add_api_route(
            path="/{uuid}",
            endpoint=self._delete_handler(),
            methods=["DELETE"],
            response_model=dict,
            summary=f"Delete {tag} by UUID",
            dependencies=[Depends(self.auth_wrapper.with_access([UserAccess.ADMIN]))]
        )

    def _create_handler(self):
        async def create(model: self.request_model = Body(...)) -> JSONResponse:
            self.logger.log_info("Creating entity")
            service_response: ServiceResponse = await self.service.create(request=model)
            return self.make_response(service_response)
        return create

    def _get_handler(self):
        async def get(uuid: UUID) -> JSONResponse:
            self.logger.log_info(f"Reading entity {uuid}")
            service_response: ServiceResponse = await self.service.get(uuid)
            return self.make_response(service_response)
        return get

    def _list_handler(self):
        async def list_entities(page: int = Query(...), per_page: int = Query(10)) -> JSONResponse:
            self.logger.log_info(f"Listing entities page: {page}, per_page: {per_page}")
            service_response: ServiceResponse = await self.service.list(page=page, per_page=per_page)
            return self.make_response(service_response)
        return list_entities

    def _update_handler(self):
        async def update(uuid: UUID, model: self.request_model = Body(...)) -> JSONResponse:
            self.logger.log_info(f"Updating entity {uuid}")
            service_response: ServiceResponse = await self.service.update(obj_id=uuid, request=model)
            return self.make_response(service_response)
        return update

    def _delete_handler(self):
        async def delete(uuid: UUID) -> JSONResponse:
            self.logger.log_info(f"Deleting entity {uuid}")
            service_response: ServiceResponse = await self.service.delete(obj_id=uuid)
            return self.make_response(service_response)
        return delete
    
    def make_response(self, service_response: ServiceResponse) -> JSONResponse:
        return JSONResponse(
            status_code=service_response.status,
            content=jsonable_encoder({
                'payload': service_response.payload or {},
                'message': service_response.message
            })
        )