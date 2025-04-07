from api.controllers.models.address.address_request_model import AddressRequestModel
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.domain.entities.address import Address
from api.infrastructure.repositories.address_repository import AddressRepository
from api.services.base_service import BaseService


class AddressService(BaseService[AddressRequestModel, AddressResponseModel, Address]):
    def __init__(self, address_repository: AddressRepository):
        super().__init__(address_repository, Address)