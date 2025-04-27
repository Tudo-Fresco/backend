from api.controllers.models.store.store_response_model import StoreResponseModel
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.exceptions.external_service_exception import ExternalServiceException
from api.shared.validator import Validator
from api.shared.logger import Logger
import http.client
import json
from datetime import datetime


class ReceitaClient:
    BASE_HOST = "receitaws.com.br"
    BASE_PATH = "/v1/cnpj"

    def __init__(self):
        self.logger = Logger('ReceitaClient')
        self.validator = Validator()

    async def get_by_cnpj(self, cnpj: str) -> StoreResponseModel:
        self.validator.on(cnpj, 'CNPJ').cnpj_is_valid(f'O valor informado: {cnpj} não é um CNPJ válido').check()
        data = await self._fetch_data_from_receita(cnpj)
        address = AddressResponseModel(
            zip_code=data.get('cep', None),
            street_address=data.get('logradouro', None),
            number=data.get('numero', None),
            neighbourhood=data.get('bairro', None),
            city=data.get('municipio', None),
            province=data.get('uf', None),
            latitude=None,
            longitude=None,
            additional_info=data.get('complemento', None)
        )

        store_response = StoreResponseModel(
            cnpj=data.get('cnpj', None),
            address=address,
            reputation=None,
            trade_name=data.get('fantasia', None),
            legal_name=data.get('nome', None),
            owner=None, 
            legal_phone_contact=data.get('telefone', None),
            preferred_phone_contact=None,
            legal_email_contact=data.get('email', None),
            preferred_email_contact=None,
            opening_date=datetime.strptime(
                data.get('abertura', '01/01/2000'), "%d/%m/%Y"
            ).date() if data.get('abertura') else None,
            size=data.get('porte', None),
            legal_nature=data.get('natureza_juridica', None),
            cnae_code=data.get('atividade_principal', [{}])[0].get('code', None),
            branch_classification= data.get('tipo', None)
        )

        return store_response

    async def _fetch_data_from_receita(self, cnpj: str) -> dict:
        conn = http.client.HTTPSConnection(self.BASE_HOST)
        cleaned_cnpj = cnpj.replace('/', '').replace('.', '').replace('-', '')
        path = f"{self.BASE_PATH}/{cleaned_cnpj}"
        self.logger.log_info(f"Fetching the Cnpj: {cnpj} from the gov")
        try:
            conn.request("GET", path)
            response = conn.getresponse()
            if response.status != 200:
                error_message = response.read().decode()
                self.logger.log_error(f"Error while fetching the Cnpj {cnpj}: {response.status} - {error_message}")
                raise ExternalServiceException(f"Error while fetching the Cnpj {cnpj}: {response.status}")
            data: dict = json.loads(response.read())
            if data.get('status') == 'ERROR':
                error_message = data.get('message', 'Unknown error')
                self.logger.log_error(f"Error in API response: {error_message}")
                raise ExternalServiceException(f"Error in API response: {error_message}")
            self.logger.log_info(f"Cnpj {cnpj} found.")
            return data
        finally:
            conn.close()