import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID
from datetime import datetime, date
from http import HTTPStatus
from fastapi.responses import JSONResponse
from api.controllers.demand_controller import DemandController
from api.controllers.models.demand.demand_request_model import DemandRequestModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.enums.demand_status import DemandStatus
from api.enums.product_type import ProductType
from api.enums.gender_type import GenderType
from api.enums.user_access import UserAccess
from api.enums.user_verification_status import UserVerificationStatus
from api.services.service_response import ServiceResponse


class TestDemandController(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.mock_service = MagicMock()
        self.mock_auth_wrapper = MagicMock()
        self.user = UserResponseModel(
            uuid=str(UUID('12345678-1234-5678-1234-567812345678')),
            name='Gabriel Voltolini',
            email='gabriel@example.com',
            date_of_birth=date(2000, 1, 1),
            gender=GenderType.MALE,
            phone_number='+55 47 99999-9999',
            profile_picture='https://example.com/profile.jpg',
            user_access=UserAccess.STORE_OWNER,
            verification_status=UserVerificationStatus.EMAIL_AND_PHONE
        )
        self.mock_auth_wrapper.with_access.return_value = AsyncMock(return_value=self.user)
        self.controller = DemandController(service=self.mock_service, auth_wrapper=self.mock_auth_wrapper)

    async def test_create_handler_success(self) -> None:
        request = DemandRequestModel(
            store_uuid=UUID('1f4e1f4b-ea47-4d3c-8901-cdcd7bb8e10a'),
            product_uuid=UUID('2d7f5e9f-fb71-4fd2-b929-2d6d7a99fa7a'),
            responsible_uuid=UUID('3f8d2f7e-3a14-44db-8f69-093eb8f123b1'),
            needed_count=50,
            description='50 packs of organic rice',
            deadline=datetime(2025, 10, 1, 12, 0, 0),
            status=DemandStatus.OPENED,
            minimum_count=1
        )
        self.mock_service.create = AsyncMock(return_value=ServiceResponse(
            status=HTTPStatus.CREATED,
            message="Demand created",
            payload={"id": "abc-123"}
        ))
        endpoint = self.controller._create_handler()
        response = await endpoint(model=request)
        self.mock_service.create.assert_awaited_once()
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn("Demand created", response.body.decode())

    async def test_get_handler_success(self) -> None:
        self.mock_service.get = AsyncMock(return_value=ServiceResponse(
            status=HTTPStatus.OK,
            message="Demand retrieved",
            payload={"id": "abc-123"}
        ))
        endpoint = self.controller._get_handler()
        uuid = UUID("11111111-2222-3333-4444-555566667777")
        store_uuid = UUID("99999999-8888-7777-6666-555544443333")
        response = await endpoint(uuid=uuid, store_uuid=store_uuid, user=self.user)
        self.mock_service.get.assert_awaited_once_with(uuid, self.user, store_uuid)
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("Demand retrieved", response.body.decode())

    async def test_list_by_store_handler_success(self) -> None:
        self.mock_service.list_by_store = AsyncMock(return_value=ServiceResponse(
            status=HTTPStatus.OK,
            message="Demands listed",
            payload=[{"id": "abc"}, {"id": "def"}]
        ))
        endpoint = self.controller._list_by_store_handler()
        store_uuid = UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeffffffff")
        response = await endpoint(
            store_uuid=store_uuid,
            page=1,
            per_page=10,
            radius_meters=5000,
            product_type=ProductType.ANY,
            status=DemandStatus.ANY
        )
        self.mock_service.list_by_store.assert_awaited_once()
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("Demands listed", response.body.decode())

    def test_routes_and_auth_wrapper_setup(self) -> None:
        controller = DemandController(service=self.mock_service, auth_wrapper=self.mock_auth_wrapper)
        expected_roles = {UserAccess.STORE_OWNER, UserAccess.ADMIN}
        for call_args in self.mock_auth_wrapper.with_access.call_args_list:
            actual_roles = set(call_args.args[0])
            assert expected_roles.issubset(actual_roles), f"Call missing expected roles: {actual_roles}"
        routes = {route.path: route for route in controller.router.routes}
        assert '/demand/list-by-store' in routes
        assert '/demand/by-uuid/{uuid}' in routes
        list_route = routes['/demand/list-by-store']
        assert list_route.methods == {'GET'}
        get_route = routes['/demand/by-uuid/{uuid}']
        assert get_route.methods == {'GET'}