from typing import TypeVar, Generic, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.domain.entities.base_entity import BaseEntity
from api.exceptions.not_found_exception import NotFoundException
from api.infrastructure.models.base_model import BaseModel
from api.infrastructure.repositories.i_repository import IRepository
from api.shared.logger import Logger

T = TypeVar('T', bound=BaseEntity)
M = TypeVar('M', bound=BaseModel)

class BaseRepository(IRepository[T], Generic[T, M]):

    def __init__(self, session: AsyncSession, model_class: type[M]):
        self.session = session
        self.model_class = model_class
        logger_name = f'{model_class.__name__}Rpository'
        logger_name = logger_name.replace('Model', '')
        self.logger = Logger(logger_name)

    async def create(self, obj: T) -> None:
            model = self.model_class()
            model.from_entity(obj)
            self.session.add(model)
            await self.session.commit()

    async def get(self, obj_id: UUID) -> T:
        self.logger.log_debug(f'Retrieving record: {obj_id}')
        result = await self.session.execute(
            select(self.model_class).filter_by(uuid=obj_id, active=True)
        )
        model = result.scalars().one_or_none()
        if model is None:
            self.logger.log_warning(f'No active record found for UUID: {obj_id}')
            raise NotFoundException(f'Nenhum registro com o id {obj_id} foi encontrado')
        return model.to_entity()

    async def list(self, page: int = 1, per_page: int = 10) -> List[T]:
        self.logger.log_debug(f'Listing records (page {page}, per_page {per_page})')
        if page < 1:
            page = 1
        query = select(self.model_class).filter_by(active=True).offset((page - 1) * per_page).limit(per_page)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def update(self, obj: T) -> None:
        self.logger.log_debug(f'Updating the record: {obj.uuid}')
        await self.get(obj.uuid)
        model = self.model_class()
        model.from_entity(obj)
        await self.session.merge(model)
        await self.session.commit()
        self.logger.log_debug(f'The record {obj.uuid} was updated successfully')