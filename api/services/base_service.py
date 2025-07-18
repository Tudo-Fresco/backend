from api.controllers.models.base_request_model import BaseRequestModel
from api.controllers.models.base_response_model import BaseResponseModel
from api.domain.entities.base_entity import BaseEntity
from api.exceptions.not_found_exception import NotFoundException
from api.infrastructure.repositories.i_repository import IRepository
from api.services.i_service import IService
from api.services.service_exception_catcher import ServiceExceptionCatcher
from api.services.service_response import ServiceResponse
from api.shared.logger import Logger
from typing import TypeVar, Generic, List
from http import HTTPStatus
from uuid import UUID


REQUEST = TypeVar('REQUEST', bound=BaseRequestModel)
RESPONSE = TypeVar('RESPONSE', bound=BaseResponseModel)
T = TypeVar('T', bound=BaseEntity)

class BaseService(IService[REQUEST, RESPONSE], Generic[REQUEST, RESPONSE, T]):

    catch = ServiceExceptionCatcher('ServiceExceptionCatcher')

    def __init__(self, repository: IRepository[T], entity: type[T], response_model: type[RESPONSE]):
        self.entity = entity
        self.response_model = response_model
        self.logger = Logger(__class__.__name__)
        self.repository: IRepository[T] = repository

    @catch
    async def create(self, request: REQUEST) -> ServiceResponse[RESPONSE]:
        self.logger.log_info('Creating a new record')
        entity: BaseEntity = self.entity(**request.model_dump())
        entity.validate()
        await self.repository.create(entity)
        response = self.response_model(**entity.to_dict())
        return ServiceResponse(status=HTTPStatus.CREATED, message=f'O registro {entity.uuid} foi criado com sucesso', payload=response)

    @catch
    async def get(self, obj_id: UUID) -> ServiceResponse[RESPONSE]:
        self.logger.log_info(f'Reading from id {obj_id}')
        entity = await self.repository.get(obj_id)
        self._raise_not_found_when_none(entity, obj_id)
        response = self.response_model(**entity.to_dict())
        return ServiceResponse(status=HTTPStatus.OK, message=f'O registro {obj_id} foi encontrado com sucesso', payload=response)

    @catch
    async def list(self, page: int = 1, per_page: int = 10) -> ServiceResponse[List[RESPONSE]]:
        self.logger.log_info(f'Reading many. Page: {page}, per page: {per_page}')
        entities = await self.repository.list(page, per_page)
        entities_response = self._convert_many_to_response(entities)
        return ServiceResponse(status=HTTPStatus.OK, message=f'Leu {len(entities_response)} registros com sucesso', payload=entities_response)

    @catch
    async def update(self, obj_id: UUID, request: REQUEST) -> ServiceResponse[RESPONSE]:
        self.logger.log_info(f'Updating the record {obj_id}')
        original_entity: BaseEntity = await self.repository.get(obj_id)
        self._raise_not_found_when_none(original_entity, obj_id)
        original_entity.update(**request.model_dump())
        await self.repository.update(original_entity)
        response = self.response_model(**original_entity.to_dict())
        return ServiceResponse(status=HTTPStatus.OK, message='O registro foi atualizado com sucesso', payload=response)

    @catch
    async def delete(self, obj_id: UUID) -> ServiceResponse[None]:
        self.logger.log_info(f'Deleting the record {obj_id}')
        original_entity: BaseEntity = await self.repository.get(obj_id)
        self._raise_not_found_when_none(original_entity, obj_id)
        original_entity.deactivate()
        await self.repository.update(original_entity)
        return ServiceResponse(status=HTTPStatus.OK, message='Excluído com sucesso', payload=None)

    def _raise_not_found_when_none(self, entity: BaseEntity, expected_id: UUID) -> None:
        if not entity:
            raise NotFoundException(f'O registro {expected_id} não foi encontrado')

    def _convert_many_to_response(self, entities: List[BaseEntity]) -> List[RESPONSE]:
        entities_response = []
        for entity in entities:
            entity_dict = entity.to_dict()
            response = self.response_model(**entity_dict)
            entities_response.append(response)
        return entities_response