import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
from http import HTTPStatus
from api.services.address_service import AddressService
from api.controllers.models.address.address_request_model import AddressRequestModel
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.controllers.models.address.coordinates_response_model import CoordinatesResponseModel
from api.domain.entities.address import Address
from api.infrastructure.repositories.address_repository import AddressRepository
from api.services.service_response import ServiceResponse


class TestAddressService(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.repository = AsyncMock(spec=AddressRepository)
        self.address_service = AddressService(self.repository)
        self.fake_uuid = str(uuid4())

    def make_address_request(self) -> AddressRequestModel:
        return AddressRequestModel(
            zip_code='12345-678',
            street_address='Av. Paulista',
            latitude=-23.561684,
            longitude=-46.655981,
            province='São Paulo',
            city='São Paulo',
            neighbourhood='Bela Vista',
            number='1000',
            additional_info='Apt 101'
        )

    def make_address_response(self) -> AddressResponseModel:
        return AddressResponseModel(
            uuid=self.fake_uuid,
            zip_code='12345-678',
            street_address='Av. Paulista',
            latitude=-23.561684,
            longitude=-46.655981,
            province='São Paulo',
            city='São Paulo',
            neighbourhood='Bela Vista',
            number='1000',
            additional_info='Apt 101'
        )

    def make_address_entity(self) -> MagicMock:
        address = MagicMock(spec=Address)
        address.uuid = self.fake_uuid
        address.to_dict.return_value = {
            'uuid': self.fake_uuid,
            'zip_code': '12345-678',
            'street_address': 'Av. Paulista',
            'latitude': -23.561684,
            'longitude': -46.655981,
            'province': 'São Paulo',
            'city': 'São Paulo',
            'neighbourhood': 'Bela Vista',
            'number': '1000',
            'additional_info': 'Apt 101'
        }
        return address

    @patch('api.services.address_service.CorreiosClient')
    async def test_fresh_fill_success(self, mock_correios_cls) -> None:
        expected_response = self.make_address_response()
        mock_client = AsyncMock()
        mock_client.get_by_cep.return_value = expected_response
        mock_correios_cls.return_value = mock_client
        response = await self.address_service.fresh_fill("12345-678")
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(response.payload, expected_response)
        mock_client.get_by_cep.assert_awaited_once_with("12345-678")

    @patch('api.services.address_service.CorreiosClient')
    async def test_fresh_fill_failure(self, mock_correios_cls) -> None:
        mock_client = AsyncMock()
        mock_client.get_by_cep.side_effect = Exception("timeout")
        mock_correios_cls.return_value = mock_client
        response = await self.address_service.fresh_fill("00000-000")
        self.assertEqual(response.status, HTTPStatus.INTERNAL_SERVER_ERROR)

    @patch('api.services.address_service.OpenStreetMapsClient')
    async def test_get_approximate_coordinates_success(self, mock_osm_cls) -> None:
        address = self.make_address_entity()
        self.repository.get.return_value = address
        mock_client = AsyncMock()
        mock_client.get_coordinates.return_value = (-23.561684, -46.655981)
        mock_osm_cls.return_value = mock_client
        response = await self.address_service.get_approximate_coordinates(self.fake_uuid)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.payload, CoordinatesResponseModel)
        self.assertEqual(response.payload.latitude, -23.561684)
        self.assertEqual(response.payload.longitude, -46.655981)

    async def test_create_success(self) -> None:
        request = self.make_address_response()
        address = self.make_address_entity()
        self.repository.create.return_value = None
        self.repository.update.return_value = None
        self.address_service.repository.get = AsyncMock(return_value=address)
        with patch.object(Address, "validate"), \
             patch.object(Address, "update"), \
             patch.object(self.address_service, "get_approximate_coordinates", return_value=ServiceResponse(
                 status=HTTPStatus.OK,
                 message="Coordinates found",
                 payload=CoordinatesResponseModel(latitude=1.1, longitude=2.2)
             )), \
             patch.object(Address, "to_dict", return_value=address.to_dict()):
            response = await self.address_service.create(request)
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.repository.create.assert_awaited_once()
        self.repository.update.assert_awaited()

    async def test_update_success(self) -> None:
        request = self.make_address_request()
        address = self.make_address_entity()
        self.repository.get.return_value = address
        self.repository.update.return_value = None
        with patch.object(Address, "update"), \
             patch.object(Address, "validate"), \
             patch.object(Address, "to_dict", return_value=address.to_dict()), \
             patch.object(self.address_service, "_update_coordinates", return_value=None):
            response = await self.address_service.update(self.fake_uuid, request)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.repository.update.assert_awaited_once()

    async def test_get_success(self) -> None:
        address = self.make_address_entity()
        self.repository.get.return_value = address
        response = await self.address_service.get(self.fake_uuid)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(response.payload.uuid, self.fake_uuid)

    async def test_list_success(self) -> None:
        address = self.make_address_entity()
        self.repository.list.return_value = [address]
        response = await self.address_service.list()
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(len(response.payload), 1)
        self.assertEqual(response.payload[0].uuid, self.fake_uuid)

    async def test_delete_success(self) -> None:
        address = self.make_address_entity()
        self.repository.get.return_value = address
        with patch.object(address, 'deactivate') as mock_deactivate:
            response = await self.address_service.delete(self.fake_uuid)
        self.assertEqual(response.status, HTTPStatus.OK)
        mock_deactivate.assert_called_once()
        self.repository.update.assert_awaited_once()