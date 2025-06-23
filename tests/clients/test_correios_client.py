import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from api.clients.correios_client import CorreiosClient
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.exceptions.external_service_exception import ExternalServiceException
from api.shared.logger import Logger
from api.shared.validator import Validator
import json


class TestCorreiosClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = CorreiosClient()

    @patch.object(Validator, 'on')
    @patch.object(CorreiosClient, '_fetch_data_from_correios', new_callable=AsyncMock)
    async def test_get_by_cep_returns_address_response_model(self, mock_fetch: MagicMock, mock_validator_on: MagicMock) -> None:
        cep = '01001-000'
        mock_validator_on.return_value.cep_is_valid.return_value.check.return_value = None
        mock_fetch.return_value = {
            'cep': '01001-000',
            'logradouro': 'Praça da Sé',
            'bairro': 'Sé',
            'localidade': 'São Paulo',
            'uf': 'SP',
            'complemento': 'lado ímpar'
        }

        result = await self.client.get_by_cep(cep)

        self.assertIsInstance(result, AddressResponseModel)
        self.assertEqual(result.zip_code, '01001-000')
        self.assertEqual(result.street_address, 'Praça da Sé')
        self.assertEqual(result.neighbourhood, 'Sé')
        self.assertEqual(result.city, 'São Paulo')
        self.assertEqual(result.province, 'SP')
        self.assertEqual(result.additional_info, 'lado ímpar')
        self.assertIsNone(result.number)
        self.assertIsNone(result.latitude)
        self.assertIsNone(result.longitude)

    @patch('http.client.HTTPSConnection')
    @patch.object(Logger, 'log_info')
    @patch.object(Logger, 'log_error')
    async def test_fetch_data_from_correios_successful_response(self, mock_log_error: MagicMock, mock_log_info: MagicMock, mock_https_conn_cls: MagicMock) -> None:
        cep = '01001000'
        mock_conn = MagicMock()
        mock_https_conn_cls.return_value = mock_conn
        response_data = {
            'cep': '01001-000',
            'logradouro': 'Praça da Sé',
            'bairro': 'Sé',
            'localidade': 'São Paulo',
            'uf': 'SP',
            'complemento': ''
        }
        response_mock = MagicMock()
        response_mock.status = 200
        response_mock.read.side_effect = [
            json.dumps(response_data).encode('utf-8'),
            json.dumps(response_data).encode('utf-8')
        ]
        mock_conn.getresponse.return_value = response_mock
        result = await self.client._fetch_data_from_correios(cep)
        mock_https_conn_cls.assert_called_once_with('viacep.com.br')
        mock_conn.request.assert_called_once_with('GET', f'/ws/{cep}/json/')
        mock_conn.getresponse.assert_called_once()
        mock_log_info.assert_any_call(f'Requesting ZIP code {cep} from Correios API...')
        mock_log_info.assert_any_call(f'ZIP code {cep} successfully retrieved.')
        mock_conn.close.assert_called_once()
        self.assertEqual(result, response_data)
        mock_log_error.assert_not_called()

    @patch('http.client.HTTPSConnection')
    @patch.object(Logger, 'log_error')
    async def test_fetch_data_from_correios_http_error(self, mock_log_error: MagicMock, mock_https_conn_cls: MagicMock) -> None:
        cep = '01001000'
        mock_conn = MagicMock()
        mock_https_conn_cls.return_value = mock_conn
        response_mock = MagicMock()
        response_mock.status = 500
        response_mock.read.return_value = b'Server error'
        mock_conn.getresponse.return_value = response_mock
        with self.assertRaises(ExternalServiceException) as cm:
            await self.client._fetch_data_from_correios(cep)
        mock_log_error.assert_any_call(f'HTTP error when fetching ZIP code {cep}: 500 - Server error')
        self.assertEqual(mock_log_error.call_count, 2)
        mock_conn.close.assert_called_once()
        self.assertIn('Erro ao consultar o CEP', str(cm.exception))

    @patch('http.client.HTTPSConnection')
    @patch.object(Logger, 'log_info')
    async def test_fetch_data_from_correios_not_found(self, mock_log_info: MagicMock, mock_https_conn_cls: MagicMock) -> None:
        cep = '01001000'
        mock_conn = MagicMock()
        mock_https_conn_cls.return_value = mock_conn
        response_data = {'erro': True}
        response_mock = MagicMock()
        response_mock.status = 200
        response_mock.read.side_effect = [
            json.dumps(response_data).encode('utf-8'),
            json.dumps(response_data).encode('utf-8')
        ]
        mock_conn.getresponse.return_value = response_mock
        with self.assertRaises(ExternalServiceException) as cm:
            await self.client._fetch_data_from_correios(cep)
        mock_log_info.assert_any_call(f'ZIP code {cep} not found.')
        mock_conn.close.assert_called_once()
        self.assertIn('não foi encontrado', str(cm.exception))

    @patch('http.client.HTTPSConnection')
    @patch.object(Logger, 'log_error')
    async def test_fetch_data_from_correios_raises_external_service_exception_on_unexpected_error(self, mock_log_error: MagicMock, mock_https_conn_cls: MagicMock) -> None:
        cep = '01001000'
        mock_conn = MagicMock()
        mock_https_conn_cls.return_value = mock_conn
        mock_conn.request.side_effect = Exception('Connection failure')
        with self.assertRaises(ExternalServiceException) as cm:
            await self.client._fetch_data_from_correios(cep)
        mock_log_error.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertIn('Erro inesperado ao consultar o CEP', str(cm.exception))