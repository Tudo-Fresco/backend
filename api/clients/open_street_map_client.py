from api.domain.entities.address import Address
from api.exceptions.external_service_exception import ExternalServiceException
from api.exceptions.not_found_exception import NotFoundException
from api.shared.logger import Logger
from api.shared.validator import Validator
import http.client
import urllib.parse
import json


class OpenStreetMapsClient:
    BASE_HOST = 'nominatim.openstreetmap.org'
    BASE_PATH = '/search'

    def __init__(self):
        self.logger = Logger('NominatimClient')
        self.validator = Validator()

    async def get_coordinates(self, address: Address) -> tuple[float, float]:
        """Retrieve latitude and longitude for a given address using Nominatim API."""
        self._validate_address(address)
        query = self._build_query(address)
        self.logger.log_info(f'Consultando coordenadas para: {query}')
        try:
            conn = http.client.HTTPSConnection(self.BASE_HOST)
            path = f'{self.BASE_PATH}?q={urllib.parse.quote(query)}&format=json&limit=1'
            headers = {
                'User-Agent': 'TudoFresco/1.0 (gbrl.volt@gmail.com)'
            }
            conn.request('GET', path, headers=headers)
            response = conn.getresponse()
            if response.status != 200:
                error_message = response.read().decode()
                self.logger.log_error(f'Erro HTTP {response.status}: {error_message}')
                raise ExternalServiceException(f'Erro ao buscar coordenadas: {response.status}')
            result = json.loads(response.read())
            if not result:
                raise NotFoundException('Endereço não encontrado no Nominatim.')
            lat = float(result[0]['lat'])
            lon = float(result[0]['lon'])
            self.logger.log_info(f'Coordenadas obtidas: lat={lat}, lon={lon}')
            return lat, lon
        except Exception as ex:
            self.logger.log_error(f'Erro inesperado ao consultar endereço: {ex}')
            raise ExternalServiceException(f'Erro inesperado ao consultar coordenadas: {ex}')
        finally:
            conn.close()

    def _validate_address(self, address: Address):
        """Validate that required address fields are not empty."""
        self.validator.on(address.street_address, 'Endereço').not_empty('Endereço não pode ser vazio.')
        self.validator.on(address.city, 'Cidade').not_empty('Cidade não pode ser vazia.')
        self.validator.on(address.province, 'Estado').not_empty('Estado não pode ser vazio.')
        self.validator.check()

    def _build_query(self, address: Address) -> str:
        """Build a query string from address components for the Nominatim API."""
        parts = []
        street_with_number = address.street_address
        if address.number:
            street_with_number = street_with_number + ' ' + address.number
        parts.append(street_with_number)
        if address.city:
            parts.append(address.city)
        if address.province:
            parts.append(address.province)
        parts.append('Brasil')
        return ', '.join(parts)