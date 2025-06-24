import unittest
from unittest.mock import MagicMock, AsyncMock
from uuid import UUID
from fastapi.responses import JSONResponse
from api.controllers.models.user.user_response_model import UserResponseModel
from api.controllers.reel_controller import ReelController
from api.enums.user_access import UserAccess
from api.enums.product_type import ProductType
from api.enums.demand_status import DemandStatus
from api.services.service_response import ServiceResponse


class TestReelController(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.mock_service = MagicMock()
        self.mock_auth_wrapper = MagicMock()
        self.controller = ReelController(service=self.mock_service, auth_wrapper=self.mock_auth_wrapper)

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

    def test_routes_and_auth_wrapper(self) -> None:
        expected_roles = {UserAccess.STORE_OWNER, UserAccess.ADMIN}
        for call_args in self.mock_auth_wrapper.with_access.call_args_list:
            actual_roles = set(call_args.args[0])
            self.assertTrue(
                expected_roles.issubset(actual_roles),
                f"Call to with_access missing expected roles: {actual_roles}"
            )

        routes = {route.path: route for route in self.controller.router.routes}
        self.assertIn("/reel/posts", routes)
        self.assertEqual(routes["/reel/posts"].methods, {"GET"})

    async def test_get_posts_handler_success(self) -> None:
        self.mock_service.get_posts = AsyncMock(return_value=ServiceResponse(
            status=200,
            message="Posts found",
            payload=[{"id": "post1"}, {"id": "post2"}]
        ))
        endpoint = self.controller._posts_handler()
        store_uuid = UUID("11111111-2222-3333-4444-555566667777")
        response = await endpoint(
            store_uuid=store_uuid,
            page=1,
            per_page=10,
            radius_meters=10000,
            product_type=ProductType.ANY,
            status=DemandStatus.ANY,
            user=self.user
        )
        self.mock_service.get_posts.assert_awaited_once_with(
            user=self.user,
            store_uuid=store_uuid,
            status=DemandStatus.ANY,
            page=1,
            per_page=10,
            radius_meters=10000,
            product_type=ProductType.ANY
        )
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Posts found", response.body.decode())
