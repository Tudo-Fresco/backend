from typing import Dict, TypeVar
from sqlalchemy import Column, DateTime, Boolean, inspect
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4, UUID

Base = declarative_base()
T = TypeVar("T")

class BaseModel(Base):
    __abstract__ = True
    
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def to_dict(self) -> Dict:
        """Convert the model instance to a dictionary."""
        result = {}
        for column in inspect(self).c:
            result[column.key] = getattr(self, column.key)
        return result

    def to_entity(self: T) -> T:
        """Convert the SQLAlchemy model to an entity."""
        return self.__class__(**self.to_dict())