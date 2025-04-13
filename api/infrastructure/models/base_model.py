from abc import abstractmethod
from sqlalchemy import Column, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from uuid import uuid4
from datetime import datetime
import pytz
from api.domain.entities.base_entity import BaseEntity

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), onupdate=lambda: datetime.now(pytz.utc), nullable=False)

    def from_entity(self, entity: BaseEntity) -> None:
        '''Handle common fields for all models derived from BaseModel.'''
        self.uuid = entity.uuid
        self.active = entity.active
        self.created_at = entity.created_at
        self.updated_at = entity.updated_at
        self._from_entity(entity)

    def to_entity(self) -> BaseEntity:
        '''Handle common fields and delegate specific fields to child class.'''
        entity = self._to_entity()
        entity.set_base_properties(self.uuid, self.active, self.created_at, self.updated_at)
        return entity

    @abstractmethod
    def _from_entity(self, entity: BaseEntity) -> None:
        '''Child classes implement this to handle their specific fields.'''
        raise NotImplementedError('The method _from_entity must be implemented')

    @abstractmethod
    def _to_entity(self) -> BaseEntity:
        '''Child classes implement this to construct their specific entity.'''
        raise NotImplementedError('The method _to_entity must be implemented')