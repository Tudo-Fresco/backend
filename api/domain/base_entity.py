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
    __abstract__ = True

    uuid = Column(UUID, primary_key=True, default=uuid4, unique=True, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __init__(self, **kwargs):
        """
        Constructor method to initialize attributes dynamically.
        """
        kwargs['uuid'] = self._enforce_uuid(kwargs.get('uuid', uuid4()))
        kwargs['active'] = kwargs.get('active', True)
        kwargs['created_at'] = self._enforce_datetime(kwargs.get('created_at', datetime.now(timezone.utc)))
        kwargs['updated_at'] = self._enforce_datetime(kwargs.get('updated_at', datetime.now(timezone.utc)))
        super().__init__(**kwargs)
        self._initialized = True

    @abstractmethod
    def validate(self):
        raise NotImplementedError("This function is not implemented")

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def to_dict(self) -> dict:
        result = {}
        properties: dict = self.__dict__.items()
        for key, value in properties:
            if key.startswith('_'):
                continue
            if isinstance(value, PythonUUID):
                result[key] = str(value)
            elif isinstance(value, enum.Enum):
                result[key] = value.value
            elif isinstance(value, BaseEntity):
                result[key] = value.to_dict()
            elif isinstance(value, list) and all(isinstance(i, BaseEntity) for i in value):
                result[key] = []
                for val in value:
                    result[key] = val.to_dict()
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

    def __setattr__(self, name, value):
        """
        Override setattr to automatically update `updated_at`
        whenever an attribute is modified, but not during initialization.
        """
        if "_initialized" in self.__dict__:
            if name != "updated_at" and not name.startswith("_") and hasattr(self, "uuid"):  
                super().__setattr__("updated_at", datetime.now(timezone.utc))
        super().__setattr__(name, value)
    
    def _enforce_datetime(self, value) -> datetime:
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value
    
    def _enforce_uuid(self, value) -> PythonUUID:
        if isinstance(value, str):
            return PythonUUID(value)
        return value