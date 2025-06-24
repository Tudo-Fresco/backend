import unittest
from unittest.mock import AsyncMock, MagicMock
from fastapi.responses import JSONResponse
from api.controllers.models.user.user_response_model import UserResponseModel
from api.controllers.store_controller import StoreController
from api.enums.user_access import UserAccess
from api.services.service_response import ServiceResponse


class TestStoreController(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_service = MagicMock()
        self.mock_auth_wrapper = MagicMock()
        self.controller = StoreController(service=self.mock_service, auth_wrapper=self.mock_auth_wrapper)

        self.user = UserResponseModel(
            uuid="12345678-1234-5678-1234-567812345678",
            name="Gabriel Voltolini",
            email="gabriel@example.com",
            date_of_birth="2000-01-01",
            gender="MALE",
            phone_number="+55 47 99999-9999",
            profile_picture="https://example.com/profile.jpg",
            user_access=UserAccess.STORE_OWNER,
            verification_status="EMAIL_AND_PHONE"
        )

    def test_routes_and_auth_wrapper(self):
        expected_roles = {UserAccess.STORE_OWNER, UserAccess.ADMIN}
        for call_args in self.mock_auth_wrapper.with_access.call_args_list:
            actual_roles = set(call_args.args[0])
            self.assertTrue(
                expected_roles.issubset(actual_roles),
                f"Expected roles missing in with_access: {actual_roles}"
            )
        routes = {route.path: route for route in self.controller.router.routes}
        self.assertIn("/store/list-by-user", routes)
        self.assertEqual(routes["/store/list-by-user"].methods, {"GET"})
        self.assertIn("/store/fresh-fill", routes)
        self.assertEqual(routes["/store/fresh-fill"].methods, {"GET"})

    async def test_list_by_user_handler_success(self):
        self.mock_service.list_by_user = AsyncMock(return_value=ServiceResponse(
            status=200,
            message="Stores found",
            payload=[{"id": "store1"}, {"id": "store2"}]
        ))
        endpoint = self.controller._list_by_user_handler()
        response = await endpoint(page=1, per_page=10, user=self.user)
        self.mock_service.list_by_user.assert_awaited_once_with(
            user_uuid=self.user.uuid, page=1, per_page=10
        )
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Stores found", response.body.decode())

    async def test_fresh_fill_handler_success(self):
        self.mock_service.fresh_fill = AsyncMock(return_value=ServiceResponse(
            status=200,
            message="CNPJ data filled",
            payload={"cnpj": "12345678000100"}
        ))

        endpoint = self.controller._fresh_fill_handler()
        response = await endpoint(cnpj="12345678000100")
        self.mock_service.fresh_fill.assert_awaited_once_with(cnpj="12345678000100")
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("CNPJ data filled", response.body.decode())

    async def test_create_handler_sets_owner_uuid_if_missing(self):
        self.mock_service.create = AsyncMock(return_value=ServiceResponse(
            status=201,
            message="Store created",
            payload={"id": "new-store-id"}
        ))
        model = MagicMock()
        model.owner_uuid = None
        endpoint = self.controller._create_handler()
        response = await endpoint(model=model, user=self.user)
        self.assertEqual(model.owner_uuid, self.user.uuid)
        self.mock_service.create.assert_awaited_once_with(request=model)
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Store created", response.body.decode())
