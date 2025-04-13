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
            return JSONResponse(content=self.make_content(service_response))
        return create

    def _get_handler(self):
        async def get(uuid: UUID) -> JSONResponse:
            self.logger.log_info(f"Reading entity {uuid}")
            service_response: ServiceResponse = await self.service.get(uuid)
            return JSONResponse(content=self.make_content(service_response))
        return get

    def _list_handler(self):
        async def list_entities(page: int = Query(...), per_page: int = Query(10)) -> JSONResponse:
            self.logger.log_info(f"Listing entities page: {page}, per_page: {per_page}")
            service_response: ServiceResponse = await self.service.list(page=page, per_page=per_page)
            return JSONResponse(content=self.make_content(service_response))
        return list_entities

    def _update_handler(self):
        async def update(uuid: UUID, model: self.request_model = Body(...)) -> JSONResponse:
            self.logger.log_info(f"Updating entity {uuid}")
            service_response: ServiceResponse = await self.service.update(uuid=uuid, request=model)
            return JSONResponse(content=self.make_content(service_response))
        return update

    def _delete_handler(self):
        async def delete(uuid: UUID) -> JSONResponse:
            self.logger.log_info(f"Deleting entity {uuid}")
            service_response: ServiceResponse = await self.service.delete(uuid=uuid)
            return JSONResponse(content=self.make_content(service_response))
        return delete

    def make_content(self, service_response: ServiceResponse) -> dict[str, Any]:
        payload = service_response.payload
        if isinstance(payload, BaseResponseModel):
            return jsonable_encoder(payload)
        elif isinstance(payload, list) and all(isinstance(item, BaseResponseModel) for item in payload):
            return jsonable_encoder(payload)
        return jsonable_encoder({
            'payload': payload or {},
            'message': service_response.message
        })