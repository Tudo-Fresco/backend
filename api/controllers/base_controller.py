from typing import Any, Generic, TypeVar, Type, List
from uuid import UUID
from fastapi import APIRouter, Body, Query
from fastapi.responses import JSONResponse
from api.controllers.models.base_request_model import BaseRequestModel
from api.controllers.models.base_response_model import BaseResponseModel
from api.services.i_service import IService
from api.services.service_response import ServiceResponse
from api.shared.logger import Logger

RequestModelT = TypeVar('RequestModelT', bound=BaseRequestModel)
ResponseModelT = TypeVar('ResponseModelT', bound=BaseResponseModel)

class BaseController(Generic[RequestModelT, ResponseModelT]):
    def __init__(self, service: IService, request_model: Type[RequestModelT], response_model: Type[ResponseModelT], prefix: str, tag: str):
        self.service = service
        self.logger = Logger(tag)
        self.router = APIRouter(prefix=prefix, tags=[tag])
        self.request_model = request_model
        self.response_model = response_model
        self.router.add_api_route(
            path='/',
            endpoint=self.create,
            methods=['POST'],
            response_model=response_model,
            status_code=201,
            summary=f'Create {tag}',
        )
        self.router.add_api_route(
            path='/{uuid}',
            endpoint=self.get,
            methods=['GET'],
            response_model=response_model,
            summary=f'Get {tag} by UUID',
        )
        self.router.add_api_route(
            path='/',
            endpoint=self.list,
            methods=['GET'],
            response_model=List[response_model],
            summary=f'List {tag}s',
        )
        self.router.add_api_route(
            path='/{uuid}',
            endpoint=self.update,
            methods=['PUT'],
            response_model=response_model,
            summary=f'Update {tag} by UUID',
        )
        self.router.add_api_route(
            path='/{uuid}',
            endpoint=self.delete,
            methods=['DELETE'],
            response_model=dict,
            summary=f'Delete {tag} by UUID',
        )

    async def create(self, model: RequestModelT = Body(...)) -> JSONResponse:
        self.logger.info('Creating entity')
        service_response: ServiceResponse = await self.service.create(request=model)
        return JSONResponse(content=self.make_content(service_response), status_code=service_response.status)

    async def get(self, uuid: UUID) -> JSONResponse:
        self.logger.info(f'Reading entity {uuid}')
        service_response: ServiceResponse = await self.service.get(uuid)
        return JSONResponse(content=self.make_content(service_response), status_code=service_response.status)

    async def list(self, page: int = Query(...), per_page: int = Query(10)) -> JSONResponse:
        self.logger.info(f'Listing entities page: {page}, per_page: {per_page}')
        service_response: ServiceResponse = await self.service.list(page=page, per_page=per_page)
        return JSONResponse(content=self.make_content(service_response), status_code=service_response.status)

    async def update(self, uuid: UUID, model: RequestModelT = Body(...)) -> JSONResponse:
        self.logger.info(f'Updating entity {uuid}')
        service_response: ServiceResponse = await self.service.update(uuid=uuid, request=model)
        return JSONResponse(content=self.make_content(service_response), status_code=service_response.status)

    async def delete(self, uuid: UUID) -> JSONResponse:
        self.logger.info(f'Deleting entity {uuid}')
        service_response: ServiceResponse = await self.service.delete(uuid=uuid)
        return JSONResponse(content=self.make_content(service_response), status_code=service_response.status)

    def make_content(self, service_response: ServiceResponse) -> dict[str, Any]:
        payload = service_response.payload
        if isinstance(payload, BaseResponseModel):
            return payload.model_dump()
        elif isinstance(payload, list) and all(isinstance(item, BaseResponseModel) for item in payload):
            return [item.model_dump() for item in payload]
        content = {
            'payload': payload or {},
            'message': service_response.message
        }
        return content