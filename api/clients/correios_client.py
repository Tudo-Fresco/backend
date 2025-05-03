from api.controllers.models.address.address_response_model import AddressResponseModel
from api.exceptions.external_service_exception import ExternalServiceException
from api.exceptions.not_found_exception import NotFoundException
from api.shared.validator import Validator
from api.shared.logger import Logger
import http.client
import json


class CorreiosClient:
    BASE_HOST = 'viacep.com.br'
    BASE_PATH = '/ws'

    def __init__(self):
        self.logger = Logger('CorreiosClient')
        self.validator = Validator()

    async def get_by_cep(self, cep: str) -> AddressResponseModel:
        self.validator.on(cep, 'CEP').cep_is_valid(f'O CEP informado: {cep} é inválido.').check()
        data = await self._fetch_data_from_correios(cep)
        address = AddressResponseModel(
            zip_code=data.get('cep'),
            street_address=data.get('logradouro'),
            neighbourhood=data.get('bairro'),
            city=data.get('localidade'),
            province=data.get('uf'),
            additional_info=data.get('complemento') or None,
            number=None,
            latitude=None,
            longitude=None
        )
        return address

    async def _fetch_data_from_correios(self, cep: str) -> dict:
        cleaned_cep = cep.replace('-', '').strip()
        conn = http.client.HTTPSConnection(self.BASE_HOST)
        path = f'{self.BASE_PATH}/{cleaned_cep}/json/'
        self.logger.log_info(f'Requesting ZIP code {cleaned_cep} from Correios API...')
        try:
            conn.request('GET', path)
            response = conn.getresponse()
            if response.status != 200:
                error_message = response.read().decode()
                self.logger.log_error(f'HTTP error when fetching ZIP code {cleaned_cep}: {response.status} - {error_message}')
                raise ExternalServiceException(f'Erro ao consultar o CEP {cleaned_cep}: código {response.status}')
            data: dict = json.loads(response.read())
            if data.get('erro'):
                self.logger.log_info(f'ZIP code {cleaned_cep} not found.')
                raise NotFoundException(f'O CEP {cleaned_cep} não foi encontrado.')
            self.logger.log_info(f'ZIP code {cleaned_cep} successfully retrieved.')
            return data
        except Exception as ex:
            self.logger.log_error(f'Unexpected error while fetching ZIP code {cleaned_cep}: {ex}')
            raise ExternalServiceException(f'Erro inesperado ao consultar o CEP {cleaned_cep}: {ex}')
        finally:
            conn.close()
