from http import HTTPStatus
from api.clients.correios_client import CorreiosClient
from api.controllers.models.address.address_request_model import AddressRequestModel
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.domain.entities.address import Address
from api.infrastructure.repositories.address_repository import AddressRepository
from api.services.base_service import BaseService
from api.services.service_exception_catcher import ServiceExceptionCatcher
from api.services.service_response import ServiceResponse


class AddressService(BaseService[AddressRequestModel, AddressResponseModel, Address]):
    
    catch = ServiceExceptionCatcher('AddressServiceExceptionCatcher')

    def __init__(self, address_repository: AddressRepository):
        super().__init__(address_repository, Address, AddressResponseModel)

    @catch
    async def fresh_fill(self, cep: str) -> ServiceResponse[AddressResponseModel]:
        correios_client = CorreiosClient()
        partially_filled_address_response_model = await correios_client.get_by_cep(cep)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'O endereço do CEP {cep} foi encontrada com sucesso nos Correios',
            payload=partially_filled_address_response_model
        )