from typing import TypeVar
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4

from api.domain.base_entity import BaseEntity

M = TypeVar('M', bound='BaseModel')

class BaseModel(DeclarativeBase):
    __abstract__ = True

    uuid = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    active = Column(Boolean)
    created_at = Column(DateTime(timezone=True))  
    updated_at = Column(DateTime(timezone=True))

    def to_entity(self):
        '''Converts the database model to its corresponding BaseEntity.'''
        raise NotImplementedError('Subclasses must implement to_entity to map to their domain entity')
    
    @classmethod
    def from_entity(cls, entity: BaseEntity) -> "BaseModel":
        """Converts a domain entity to a database model instance."""
        raise NotImplementedError('Subclasses must implement from_entity to map to their domain entity')
    
    def _set_base_properties(self, entity: BaseEntity) -> None:
        self.uuid = entity.uuid
        self.active = entity.active
        self.created_at = entity.created_at
        self.updated_at = entity.updated_at