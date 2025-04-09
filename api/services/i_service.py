from abc import abstractmethod
from typing import TypeVar, Generic, List
from uuid import UUID
from api.controllers.models.base_request_model import BaseRequestModel
from api.controllers.models.base_response_model import BaseResponseModel
from api.services.service_response import ServiceResponse


REQUEST = TypeVar('REQUEST', bound=BaseRequestModel)
RESPONSE = TypeVar('RESPONSE', bound=BaseResponseModel)

class IService(Generic[REQUEST, RESPONSE]):
    '''Abstract base class defining the interface for entity repositories.

    This interface provides methods for basic CRUD operations on entities, with
    the expectation that implementations handle soft deletes by managing an
    'active' flag. All operations (except create) should only interact with
    active records.
    '''

    def __init__(self):
        super().__init__()

    @abstractmethod
    async def create(self, request: REQUEST) -> ServiceResponse[RESPONSE]:
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
    async def get(self, obj_id: UUID) ->  ServiceResponse[RESPONSE]:
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
    async def list(self, page: int = 1, per_page: int = 10) -> ServiceResponse[List[RESPONSE]]:
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
    async def update(self, obj_id: UUID, request: REQUEST) -> ServiceResponse[RESPONSE]:
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
    
    async def delete(self, obj_id: UUID) -> ServiceResponse[None]:
        '''Delete an existing active entity from the data store.

        Args:
            obj_id (UUID): The unique identifier of the entity to be deleted.

        Returns:
            ServiceResponse[None]: Indicates the success or failure of the operation.

        Raises:
            NotFoundException: If no active entity with the given UUID exists.
            NotImplementedError: If not implemented by a subclass.
        '''
        raise NotImplementedError("Subclasses must implement 'update'")
