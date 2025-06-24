import unittest
from unittest.mock import MagicMock, AsyncMock
from uuid import UUID
from fastapi.responses import JSONResponse
from api.controllers.models.user.user_response_model import UserResponseModel
from api.controllers.product_controller import ProductController
from api.enums.user_access import UserAccess
from api.enums.product_type import ProductType
from api.services.service_response import ServiceResponse


class TestProductController(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.mock_service = MagicMock()
        self.mock_auth_wrapper = MagicMock()
        self.controller = ProductController(service=self.mock_service, auth_wrapper=self.mock_auth_wrapper)

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

    def test_routes_and_auth_wrapper_setup(self) -> None:
        expected_roles = {UserAccess.STORE_OWNER, UserAccess.ADMIN}
        for call_args in self.mock_auth_wrapper.with_access.call_args_list:
            actual_roles = set(call_args.args[0])
            self.assertTrue(
                expected_roles.issubset(actual_roles),
                f"Auth roles missing expected roles: {actual_roles}"
            )
        routes = {route.path: route for route in self.controller.router.routes}
        self.assertIn("/product/search", routes)
        self.assertEqual(routes["/product/search"].methods, {"GET"})
        product_picture_routes = [r for r in self.controller.router.routes if r.path == "/product/product-picture"]
        methods = {m for route in product_picture_routes for m in route.methods}
        self.assertEqual(methods, {"POST", "DELETE"})

    async def test_search_handler_success(self) -> None:
        self.mock_service.list_by_name_and_type = AsyncMock(return_value=ServiceResponse(
            status=200,
            message="Found",
            payload=[{"id": 1}]
        ))
        endpoint = self.controller._search_handler()
        response = await endpoint(
            name="Arroz",
            type=ProductType.GRAIN,
            page=1,
            per_page=10,
            user=self.user
        )
        self.mock_service.list_by_name_and_type.assert_awaited_once_with(
            name="Arroz",
            type=ProductType.GRAIN,
            page=1,
            per_page=10
        )
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Found", response.body.decode())

    async def test_upload_picture_handler_success(self) -> None:
        mock_file = MagicMock()
        mock_file.filename = "image.png"
        mock_file.read = AsyncMock(return_value=b"fake-image-bytes")
        self.mock_service.upload_picture = AsyncMock(return_value=ServiceResponse(
            status=200,
            message="Uploaded",
            payload={"ok": True}
        ))
        endpoint = self.controller._upload_picture_handler()
        product_uuid = UUID("11111111-2222-3333-4444-555566667777")
        response = await endpoint(file=mock_file, product_uuid=product_uuid, user=self.user)
        self.mock_service.upload_picture.assert_awaited_once_with(
            product_uuid=product_uuid,
            image_bytes=b"fake-image-bytes",
            file_name="image.png"
        )
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Uploaded", response.body.decode())

    async def test_delete_picture_handler_success(self) -> None:
        self.mock_service.delete_picture = AsyncMock(return_value=ServiceResponse(
            status=200,
            message="Deleted",
            payload={"ok": True}
        ))
        endpoint = self.controller._delete_picture_handler()
        product_uuid = UUID("11111111-2222-3333-4444-555566667777")
        response = await endpoint(product_uuid=product_uuid, picture_index=0, user=self.user)
        self.mock_service.delete_picture.assert_awaited_once_with(
            product_uuid=product_uuid,
            image_index=0
        )
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Deleted", response.body.decode())
