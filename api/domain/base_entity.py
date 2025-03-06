from sqlalchemy import Column, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from abc import abstractmethod
from datetime import datetime, timezone
import enum
from uuid import uuid4, UUID as PythonUUID

Base = declarative_base()

class BaseEntity(Base):
    """
    Abstract base class that defines common fields for all models.
    It includes a UUID primary key, active status, and timestamps.
    """
    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this class

    uuid = Column(UUID, primary_key=True, default=uuid4, unique=True, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __init__(self, **kwargs):
        """
        Constructor method to initialize attributes dynamically.
        """
        super().__init__(**kwargs)  # Ensure SQLAlchemy handles attributes properly

    @abstractmethod
    def validate(self):
        raise NotImplementedError("This function is not implemented")

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def to_dict(self) -> dict:
        result = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            if isinstance(value, UUID):
                result[key] = str(value)
            elif isinstance(value, enum.Enum):
                result[key] = value.value
            # elif isinstance(value, BaseEntity):
            #     result[key] = value.to_dict()
            else:
                result[key] = value
        return result

    def __setattr__(self, name, value):
        """
        Override setattr to automatically update `updated_at`
        whenever an attribute is modified, but not during initialization.
        """
        super().__setattr__(name, value)
        if name != "updated_at" and not name.startswith("_") and hasattr(self, "uuid"):  
            super().__setattr__("updated_at", datetime.now(timezone.utc))
