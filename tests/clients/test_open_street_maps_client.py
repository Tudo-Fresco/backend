import unittest
from unittest.mock import patch, MagicMock
from api.clients.open_street_map_client import OpenStreetMapsClient
from api.domain.entities.address import Address
from api.exceptions.external_service_exception import ExternalServiceException


class TestOpenStreetMapsClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.client = OpenStreetMapsClient()
        self.address = Address(
            street_address="Rua das Flores",
            number="123",
            neighbourhood="Centro",
            city="São Paulo",
            province="SP",
            zip_code="01000-000",
            additional_info="",
            latitude=0,
            longitude=0
        )

    @patch('http.client.HTTPSConnection')
    @patch.object(OpenStreetMapsClient, '_validate_address')
    async def test_get_coordinates_success(self, mock_validate: MagicMock, mock_https: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"lat": "-23.55052", "lon": "-46.633308"}]'
        mock_conn.getresponse.return_value = mock_response
        mock_https.return_value = mock_conn
        lat, lon = await self.client.get_coordinates(self.address)
        self.assertEqual(lat, -23.55052)
        self.assertEqual(lon, -46.633308)
        mock_validate.assert_called_once()
        mock_conn.request.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('http.client.HTTPSConnection')
    @patch.object(OpenStreetMapsClient, '_validate_address')
    async def test_get_coordinates_not_found(self, mock_validate: MagicMock, mock_https: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'[]'
        mock_conn.getresponse.return_value = mock_response
        mock_https.return_value = mock_conn
        with self.assertRaises(ExternalServiceException) as context:
            await self.client.get_coordinates(self.address)
        self.assertIn('Endereço não encontrado no Nominatim', str(context.exception))
        mock_conn.close.assert_called_once()

    @patch('http.client.HTTPSConnection')
    @patch.object(OpenStreetMapsClient, '_validate_address')
    async def test_get_coordinates_http_error(self, mock_validate: MagicMock, mock_https: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 500
        mock_response.read.return_value = b'Internal Server Error'
        mock_conn.getresponse.return_value = mock_response
        mock_https.return_value = mock_conn
        with self.assertRaises(ExternalServiceException):
            await self.client.get_coordinates(self.address)
        mock_conn.close.assert_called_once()

    @patch('http.client.HTTPSConnection')
    @patch.object(OpenStreetMapsClient, '_validate_address')
    async def test_get_coordinates_unexpected_exception(self, mock_validate: MagicMock, mock_https: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_https.return_value = mock_conn
        mock_conn.request.side_effect = Exception('Connection failed')
        with self.assertRaises(ExternalServiceException):
            await self.client.get_coordinates(self.address)
        mock_conn.close.assert_called_once()

    def test_build_query_with_number(self) -> None:
        query = self.client._build_query(self.address)
        expected = 'Rua das Flores 123, São Paulo, SP, Brasil'
        self.assertEqual(query, expected)

    def test_build_query_without_number(self) -> None:
        self.address.number = None
        query = self.client._build_query(self.address)
        expected = 'Rua das Flores, São Paulo, SP, Brasil'
        self.assertEqual(query, expected)
