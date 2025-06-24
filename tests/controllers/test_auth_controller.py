import unittest
from unittest.mock import AsyncMock, MagicMock
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from api.controllers.auth_controller import AuthController
from api.services.service_response import ServiceResponse
from http import HTTPStatus

class TestAuthController(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.mock_auth_service = MagicMock()
        self.controller = AuthController(auth_service=self.mock_auth_service)

    async def test_login_success(self) -> None:
        expected_response = ServiceResponse(
            status=HTTPStatus.OK,
            message="Login successful",
            payload={"token": "fake-jwt-token"}
        )
        self.mock_auth_service.authenticate_user = AsyncMock(return_value=expected_response)
        form_data = OAuth2PasswordRequestForm(username="user@example.com", password="pass", scope="", client_id=None, client_secret=None)
        response = await self.controller.router.routes[0].endpoint(form_data)
        self.mock_auth_service.authenticate_user.assert_awaited_once_with(
            email="user@example.com",
            password="pass"
        )
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = response.body.decode()
        self.assertIn("Login successful", content)
        self.assertIn("fake-jwt-token", content)

    async def test_make_content_returns_correct_response(self) -> None:
        service_response = ServiceResponse(
            status=HTTPStatus.CREATED,
            message="Created",
            payload={"user_id": 1}
        )
        response = self.controller.make_content(service_response)
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        content = response.body.decode()
        self.assertIn("Created", content)
        self.assertIn("user_id", content)

