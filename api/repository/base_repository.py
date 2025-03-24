from sqlalchemy import Result
from api.infrastructure.models.base_model import BaseModel
from typing import Type, TypeVar, Generic, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):

    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self.db_session = db_session
        self.model = model

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[T]:
        async with self.db_session as session:
            result = await session.execute(
                select(self.model).offset(offset).limit(limit)
            )
            return await self._convert_to_entity_list(result)

    async def get_by_uuid(self, uuid: str) -> T:
        async with self.db_session as session:
            result = await session.execute(
                select(self.model).filter(self.model.uuid == uuid)
            )
            return await self._convert_to_entity(result)

    async def create(self, entity: T) -> T:
        async with self.db_session as session:
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            return await self._convert_to_entity(entity)

    async def update(self, entity: T) -> T:
        async with self.db_session as session:
            merged_entity = await session.merge(entity)
            await session.commit()
            await session.refresh(merged_entity)
            return await self._convert_to_entity(merged_entity)

    async def delete(self, entity: T):
        async with self.db_session as session:
            await session.delete(entity)
            await session.commit()

    async def _convert_to_entity_list(self, result: Result) -> List[T]:
        """
        Converts a list of query results to entity objects.
        """
        entities = []
        for item in result.scalars().all():
            entity = await self._convert_to_entity(item)
            entities.append(entity)
        return entities

    async def _convert_to_entity(self, item: Result | T) -> T | None:
        """
        Converts a single query result or model instance to an entity object.
        """
        if isinstance(item, Result):
            model_instance = item.scalars().first()
        else:
            model_instance = item
        if model_instance:
            return model_instance.to_entity()
        return None
