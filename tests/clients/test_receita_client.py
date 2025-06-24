import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from api.clients.receita_client import ReceitaClient
from api.controllers.models.store.store_response_model import StoreResponseModel
from api.exceptions.not_found_exception import NotFoundException

class TestReceitaClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.valid_cnpj = "12.345.678/0001-90"

    @patch("http.client.HTTPSConnection")
    @patch.object(ReceitaClient, '__init__', return_value=None)
    async def test_get_by_cnpj_success(self, mock_init: MagicMock, mock_https: MagicMock) -> None:
        client = ReceitaClient()
        client.validator = MagicMock()
        client.logger = MagicMock()
        mock_conn = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = '''{
            "cnpj": "12345678000190",
            "logradouro": "Rua Exemplo",
            "numero": "100",
            "bairro": "Centro",
            "municipio": "São Paulo",
            "uf": "SP",
            "complemento": "Sala 1",
            "fantasia": "Loja Exemplo",
            "nome": "Loja Exemplo Ltda",
            "telefone": "11999999999",
            "email": "contato@exemplo.com",
            "abertura": "01/01/2020",
            "porte": "ME",
            "natureza_juridica": "206-2",
            "atividade_principal": [{"code": "47.89-0-02"}],
            "tipo": "MATRIZ"
        }'''.encode('utf-8')
        mock_conn.getresponse.return_value = mock_response
        mock_https.return_value = mock_conn
        result = await client.get_by_cnpj(self.valid_cnpj)
        self.assertIsInstance(result, StoreResponseModel)
        self.assertEqual(result.cnpj, "12345678000190")
        self.assertEqual(result.address.city, "São Paulo")
        self.assertEqual(result.trade_name, "Loja Exemplo")
        self.assertEqual(result.opening_date, date(2020, 1, 1))
        mock_conn.close.assert_called_once()

    @patch("http.client.HTTPSConnection")
    @patch.object(ReceitaClient, '__init__', return_value=None)
    async def test_get_by_cnpj_not_found(self, mock_init: MagicMock, mock_https: MagicMock) -> None:
        client = ReceitaClient()
        client.validator = MagicMock()
        client.logger = MagicMock()

        mock_conn = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"status": "ERROR", "message": "CNPJ n\u00e3o encontrado"}'
        mock_conn.getresponse.return_value = mock_response
        mock_https.return_value = mock_conn
        with self.assertRaises(NotFoundException):
            await client.get_by_cnpj(self.valid_cnpj)
        mock_conn.close.assert_called_once()

    @patch("http.client.HTTPSConnection")
    @patch.object(ReceitaClient, '__init__', return_value=None)
    async def test_get_by_cnpj_http_error(self, mock_init: MagicMock, mock_https: MagicMock) -> None:
        client = ReceitaClient()
        client.validator = MagicMock()
        client.logger = MagicMock()
        mock_conn = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 500
        mock_response.read.return_value = b"Erro interno"
        mock_conn.getresponse.return_value = mock_response
        mock_https.return_value = mock_conn
        with self.assertRaises(NotFoundException):
            await client.get_by_cnpj(self.valid_cnpj)
        mock_conn.close.assert_called_once()

    @patch("http.client.HTTPSConnection")
    @patch.object(ReceitaClient, '__init__', return_value=None)
    async def test_get_by_cnpj_unexpected_exception(self, mock_init: MagicMock, mock_https: MagicMock) -> None:
        client = ReceitaClient()
        client.validator = MagicMock()
        client.logger = MagicMock()
        mock_conn = MagicMock()
        mock_conn.request.side_effect = Exception("Falha de conex\u00e3o")
        mock_https.return_value = mock_conn
        with self.assertRaises(NotFoundException):
            await client.get_by_cnpj(self.valid_cnpj)
        mock_conn.close.assert_called_once()