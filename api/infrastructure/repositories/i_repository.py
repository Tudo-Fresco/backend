from abc import abstractmethod
from typing import TypeVar, Generic, List, Optional
from api.domain.entities.base_entity import BaseEntity
from uuid import UUID

T = TypeVar('T', bound=BaseEntity)

class IRepository(Generic[T]):
    
    @abstractmethod
    async def create(self, obj: T) -> None:
        """Create a new entity."""
        pass
    
    @abstractmethod
    async def get(self, obj_id: str) -> Optional[T]:
        """Get an entity by its ID."""
        pass
    
    @abstractmethod
    async def list(self, page: int = 1, per_page: int = 10) -> List[T]:
        """List all entities with pagination."""
        pass
    
    @abstractmethod
    async def update(self, obj: T) -> None:
        """Update an entity."""
        pass
    
    @abstractmethod
    async def delete(self, obj_id: UUID) -> None:
        """Delete an entity by ID."""
        pass
