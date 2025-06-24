from datetime import date
import unittest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from api.controllers.auth_wrapper import AuthWrapper
from api.enums.gender_type import GenderType
from api.enums.user_access import UserAccess
from api.enums.user_verification_status import UserVerificationStatus
from api.services.service_response import ServiceResponse
from api.controllers.models.user.user_response_model import UserResponseModel


class TestAuthWrapper(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.mock_auth_service = MagicMock()
        self.auth_wrapper = AuthWrapper(auth_service=self.mock_auth_service)
        self.required_access = [UserAccess.ADMIN, UserAccess.STORE_OWNER]

    async def test_with_access_missing_credentials_raises_401(self) -> None:
        dependency = self.auth_wrapper.with_access(self.required_access)
        with self.assertRaises(HTTPException) as cm:
            await dependency(credentials=None)
        self.assertEqual(cm.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('authorization header is missing', cm.exception.detail)

    async def test_with_access_user_without_access_raises_http_exception(self) -> None:
        dependency = self.auth_wrapper.with_access(self.required_access)
        fake_token = "fake-token"
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=fake_token)
        self.mock_auth_service.verify_access = AsyncMock(
            return_value=ServiceResponse(status=status.HTTP_403_FORBIDDEN, message="Access denied", payload=None)
        )
        with self.assertRaises(HTTPException) as cm:
            await dependency(credentials=credentials)
        self.assertEqual(cm.exception.status_code, status.HTTP_403_FORBIDDEN)

    async def test_with_access_user_with_access_returns_user(self) -> None:
        dependency = self.auth_wrapper.with_access(self.required_access)
        fake_token = "valid-token"
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=fake_token)
        fake_user = UserResponseModel(
            id=1,
            name="Test User",
            email="test@example.com",
            date_of_birth=date(1990, 1, 1),
            gender=GenderType.MALE,
            phone_number="+55 47 99999-9999",
            profile_picture="https://example.com/profile.jpg",
            user_access=UserAccess.ADMIN,
            verification_status=UserVerificationStatus.EMAIL_AND_PHONE
        )
        self.mock_auth_service.verify_access = AsyncMock(return_value=ServiceResponse(
            status=200,
            message="Access granted",
            payload=fake_user
        ))
        user = await dependency(credentials)
        self.assertEqual(user, fake_user)
        self.mock_auth_service.verify_access.assert_awaited_once_with(fake_token, self.required_access)

    def test_make_response_returns_json_response(self) -> None:
        service_response = ServiceResponse(status=status.HTTP_401_UNAUTHORIZED, message="Unauthorized", payload=None)
        response = self.auth_wrapper._AuthWrapper__make_response(service_response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Unauthorized", response.body.decode())
