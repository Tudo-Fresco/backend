from abc import abstractmethod
from datetime import datetime, timezone
import enum
from typing import Any
from uuid import uuid4, UUID


class BaseEntity:

    def __init__(self, **kwargs):
        self._uuid: UUID = self._enforce_uuid(kwargs.pop('uuid', uuid4()))
        self._active: bool = kwargs.pop('active', True)
        self._created_at: datetime = self._enforce_datetime(kwargs.pop('created_at', datetime.now(timezone.utc)))
        self._updated_at: datetime = self._enforce_datetime(kwargs.pop('updated_at', datetime.now(timezone.utc)))

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def active(self) -> bool:
        return self._active

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @abstractmethod
    def validate(self) -> None:
        return None

    def activate(self) -> None:
        self._active = True
        self.update_timestamp()

    def deactivate(self) -> None:
        self._active = False
        self.update_timestamp()

    def update_timestamp(self) -> None:
        self._updated_at = datetime.now(timezone.utc)

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.update_timestamp()

    def to_dict(self) -> dict:
        result = {
            'uuid': str(self._uuid),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        properties: dict = self.__dict__.items()
        for key, value in properties:
            if key.startswith('_'):
                continue
            if isinstance(value, UUID):
                result[key] = str(value)
            elif isinstance(value, enum.Enum):
                result[key] = value.value
            elif isinstance(value, BaseEntity):
                result[key] = value.to_dict()
            elif isinstance(value, list) and all(isinstance(i, BaseEntity) for i in value):
                result[key] = [val.to_dict() for val in value]
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
    
    def set_base_properties(self, uuid: UUID, active: bool, created_at: datetime, updated_at: datetime) -> None:
        self._uuid = self._enforce_uuid(uuid)
        self._active = active
        self._created_at = self._enforce_datetime(created_at)
        self._updated_at = self._enforce_datetime(updated_at)

    def _enforce_datetime(self, value: Any) -> datetime:
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value
    
    def _enforce_uuid(self, value: Any) -> UUID:
        if isinstance(value, str):
            return UUID(value)
        return value