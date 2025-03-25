from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type, TypeVar, Generic, List
from api.shared.logger import Logger
from api.domain.base_entity import BaseEntity
from api.infrastructure.models.base_model import BaseModel
from uuid import UUID


T = TypeVar('T', bound=BaseEntity)
M = TypeVar('M', bound=BaseModel)

class BaseRepository(Generic[T, M]):

    def __init__(self, db_session: AsyncSession, model: Type[M]):
        self.db_session = db_session
        self.model = model
        self.logger = Logger(f'{T.__name__}Repository')

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[T]:
        self.logger.log_debug(f'Get all: limit {limit}, offset: {offset}')
        async with self.db_session as session:
            result = await session.execute(select(self.model).offset(offset).limit(limit))
            rows: list[M] = result.scalars().all()
            entities: list[T] = []
            self.logger.log_debug(f'Found {len(rows)} registers')
            for model in rows:
                entities.append(model.to_entity())
            return entities

    async def get_by_uuid(self, uuid: UUID) -> T | None:
        self.logger.log_debug(f'Read by UUID: {uuid}')
        async with self.db_session as session:
            result = await session.execute(select(self.model).filter(self.model.uuid == uuid))
            model_instance = result.scalars().first()
            if not model_instance:
                self.logger.log_debug('No result was found')
                return None
            self.logger.log_debug('The result was found')
            return model_instance.to_entity()

    async def create(self, entity: T) -> T:
        self.logger.log_debug('Creating a new register')
        async with self.db_session as session:
            model_instance = self.model.from_entity(entity)
            session.add(model_instance)
            await session.commit()
            await session.refresh(model_instance)
            self.logger.log_debug('The register is created')
            return model_instance.to_entity()

    async def update(self, entity: T) -> T:
        self.logger.log_debug(f'Updating the UUID: {str(entity.uuid)}')
        async with self.db_session as session:
            model_instance = self.model.from_entity(entity)
            merged_model = await session.merge(model_instance)
            await session.commit()
            await session.refresh(merged_model)
            self.logger.log_debug('The register was updated')
            return merged_model.to_entity()

    async def delete(self, entity: T):
        self.logger.log_debug(f'Deleting the UUID: {str(entity.uuid)}')
        async with self.db_session as session:
            model_instance = self.model.from_entity(entity)
            await session.delete(model_instance)
            await session.commit()
            self.logger.log_debug('The register was deleted')