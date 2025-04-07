from abc import abstractmethod
from typing import TypeVar, Generic, List
from uuid import UUID
from api.domain.entities.base_entity import BaseEntity


T = TypeVar('T', bound=BaseEntity)

class IRepository(Generic[T]):
    '''Abstract base class defining the interface for entity repositories.

    This interface provides methods for basic CRUD operations on entities, with
    the expectation that implementations handle soft deletes by managing an
    'active' flag. All operations (except create) should only interact with
    active records.
    '''

    @abstractmethod
    async def create(self, obj: T) -> None:
        '''Create a new entity in the data store.

        Args:
            obj: The entity to create. Assumes the entity’s 'active' flag is True by default.

        Returns:
            None

        Raises:
            NotImplementedError: If not implemented by a subclass.
        '''
        raise NotImplementedError("Subclasses must implement 'create'")

    @abstractmethod
    async def get(self, obj_id: UUID) -> T:
        '''Retrieve an active entity by its UUID.

        Args:
            obj_id: The UUID of the entity to retrieve.

        Returns:
            The entity if found and active.

        Raises:
            NotFoundException: If no active entity with the given UUID exists.
            NotImplementedError: If not implemented by a subclass.
        '''
        raise NotImplementedError("Subclasses must implement 'get'")

    @abstractmethod
    async def list(self, page: int = 1, per_page: int = 10) -> List[T]:
        '''List all active entities with pagination.

        Args:
            page: The page number to retrieve (1-indexed). Defaults to 1.
            per_page: The number of entities per page. Defaults to 10.

        Returns:
            A list of active entities for the specified page.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        '''
        raise NotImplementedError("Subclasses must implement 'list'")

    @abstractmethod
    async def update(self, obj: T) -> None:
        '''Update an existing active entity in the data store.

        Args:
            obj: The entity with updated data. Must match an existing active record by UUID.

        Returns:
            None

        Raises:
            NotFoundException: If no active entity with the given UUID exists.
            NotImplementedError: If not implemented by a subclass.
        '''
        raise NotImplementedError("Subclasses must implement 'update'")