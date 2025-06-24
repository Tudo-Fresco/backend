import unittest
from unittest.mock import AsyncMock, MagicMock, call
from uuid import UUID
from fastapi.responses import JSONResponse
from http import HTTPStatus
from api.controllers.address_controller import AddressController
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.controllers.models.address.coordinates_response_model import CoordinatesResponseModel
from api.services.service_response import ServiceResponse
from api.enums.user_access import UserAccess
import json


class TestAddressController(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_service = AsyncMock()
        self.mock_auth_wrapper = MagicMock()
        self.mock_auth_wrapper.with_access.return_value = MagicMock()
        self.controller = AddressController(service=self.mock_service, auth_wrapper=self.mock_auth_wrapper)

    async def test_fresh_fill_handler_returns_expected_response(self) -> None:
        cep = "12345-678"
        expected_data = AddressResponseModel(
            zip_code=cep,
            street_address="Rua Teste",
            number="10",
            neighbourhood="Centro",
            city="Cidade",
            province="SP",
            latitude=None,
            longitude=None,
            additional_info=None
        )
        service_response = ServiceResponse(
            status=HTTPStatus.OK,
            message="Success",
            payload=expected_data
        )
        self.mock_service.fresh_fill.return_value = service_response
        fresh_fill_func = self.controller._fresh_fill_handler()
        response = await fresh_fill_func(cep=cep)
        self.mock_service.fresh_fill.assert_awaited_once_with(cep=cep)
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.body.decode())
        self.assertEqual(response_data['payload']['zip_code'], cep)

    async def test_get_approximate_coordinates_handler_returns_expected_response(self) -> None:
        test_uuid = UUID("12345678-1234-5678-1234-567812345678")
        expected_data = CoordinatesResponseModel(latitude=-23.55, longitude=-46.63)
        service_response = ServiceResponse(
            status=HTTPStatus.OK,
            message="Success",
            payload=expected_data
        )
        self.mock_service.get_approximate_coordinates.return_value = service_response
        coord_func = self.controller._get_approximate_coordinates_handler()
        response = await coord_func(uuid=test_uuid)
        self.mock_service.get_approximate_coordinates.assert_awaited_once_with(test_uuid)
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.body.decode())
        self.assertAlmostEqual(response_data['payload']['latitude'], -23.55)
        self.assertAlmostEqual(response_data['payload']['longitude'], -46.63)

    def test_routes_are_configured_with_expected_paths_and_methods(self) -> None:
        routes = {route.path: route.methods for route in self.controller.router.routes}
        self.assertIn('/address/fresh-fill', routes)
        self.assertIn('GET', routes['/address/fresh-fill'])
        self.assertIn('/address/get-approximate-coordinates', routes)
        self.assertIn('GET', routes['/address/get-approximate-coordinates'])

    def test_auth_wrapper_called_with_correct_access(self):
        expected_calls = [call([UserAccess.ADMIN, UserAccess.STORE_OWNER]), call([UserAccess.ADMIN, UserAccess.STORE_OWNER])]
        self.mock_auth_wrapper.with_access.assert_has_calls(expected_calls, any_order=True)
