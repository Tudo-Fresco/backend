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
    
    @abstractmethod
    def from_entity(self, entity: BaseEntity) -> None:
        raise NotImplementedError('The method from_entity must be implemented')
    
    @abstractmethod
    def to_entity(self) -> None:
        raise NotImplementedError('The method to_entity must be implemented')