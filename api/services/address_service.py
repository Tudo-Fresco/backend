from http import HTTPStatus
from uuid import UUID
from api.clients.OpenStreetMapsClient import OpenStreetMapsClient
from api.clients.correios_client import CorreiosClient
from api.controllers.models.address.address_request_model import AddressRequestModel
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.controllers.models.address.coordinates_response_model import CoordinatesResponseModel
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
    
    @catch
    async def get_approximate_coordinates(self, uuid: UUID) -> ServiceResponse[CoordinatesResponseModel]:
        address = await self.repository.get(uuid)
        opens_street_client = OpenStreetMapsClient()
        coordinates = await opens_street_client.get_coordinates(address)
        message = f'As coordenadas aproximadas lat, lon: {coordinates} foram encontradas para o endereço {address.uuid}'
        self.logger.log_debug(message)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=message,
            payload=CoordinatesResponseModel(latitude=coordinates[0], longitude=coordinates[1])
        )