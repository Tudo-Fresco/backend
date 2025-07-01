import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import date
from fastapi import HTTPException, status
from jose import jwt

from api.services.auth_service import AuthService
from api.enums.user_access import UserAccess
from api.enums.gender_type import GenderType
from api.enums.user_verification_status import UserVerificationStatus
from api.controllers.models.user.user_response_model import UserResponseModel
from api.services.service_response import ServiceResponse


class TestAuthService(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.mock_user_service = AsyncMock()
        with patch('api.services.auth_service.EnvVariableManager') as MockEnv:
            mock_env_instance = MockEnv.return_value
            mock_env_instance.load.side_effect = lambda key, default=None, is_sensitive=False: MagicMock(
                string=lambda: "secret_key" if key == 'JWT_SECRET_KEY' else None,
                integer=lambda: 30 if key == 'USER_TOKEN_EXPIRATION_MINUTES' else None
            )
            self.auth_service = AuthService(self.mock_user_service)
        self.user = UserResponseModel(
            uuid="123e4567-e89b-12d3-a456-426614174000",
            name="Gabriel Voltolini",
            email="gabriel@example.com",
            date_of_birth=date(2000, 1, 1),
            gender=GenderType.MALE,
            phone_number="+55 47 99999-9999",
            profile_picture="https://example.com/profile.jpg",
            user_access=UserAccess.ADMIN,
            verification_status=UserVerificationStatus.EMAIL_AND_PHONE
        )

    @patch('api.services.auth_service.jwt.decode')
    async def test_verify_access_allows_any_role(self, mock_decode: MagicMock) -> None:
        mock_decode.return_value = {"sub": str(self.user.uuid), "role": self.user.user_access.value}
        self.mock_user_service.get.return_value = ServiceResponse(
            status=status.HTTP_200_OK,
            message="Found",
            payload=self.user
        )
        response = await self.auth_service.verify_access("token", [UserAccess.ANY])
        self.assertEqual(response.status, status.HTTP_200_OK)
        self.assertEqual(response.payload.email, self.user.email)
        mock_decode.assert_called_once()
        self.mock_user_service.get.assert_awaited_once_with(str(self.user.uuid))

    @patch('api.services.auth_service.PasswordHasher.verify', return_value=False)
    async def test_authenticate_user_invalid_password(self, mock_verify: MagicMock) -> None:
        mock_user_with_password = MagicMock()
        mock_user_with_password.password = "hashed_password"
        mock_user_with_password.uuid = self.user.uuid
        mock_user_with_password.email = self.user.email
        mock_user_with_password.user_access = self.user.user_access
        mock_user_with_password.to_dict.return_value = self.user.model_dump()
        self.mock_user_service.get_by_email.return_value = ServiceResponse(
            status=status.HTTP_200_OK,
            message="Success",
            payload=mock_user_with_password
        )
        response = await self.auth_service.authenticate_user("gabriel@example.com", "wrongpassword")
        self.assertEqual(response.status, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Credenciais inválidas", response.message)
        self.assertIsNone(response.payload)

    async def test_authenticate_user_user_not_found(self) -> None:
        self.mock_user_service.get_by_email.return_value = ServiceResponse(
            status=status.HTTP_200_OK,
            message="Not found",
            payload=None
        )
        response = await self.auth_service.authenticate_user("notfound@example.com", "somepass")
        self.assertEqual(response.status, status.HTTP_424_FAILED_DEPENDENCY)
        self.assertIn("não foi possível encontrar o usuário notfound@example.com", response.message.lower())
        self.assertIsNone(response.payload)

    @patch('api.services.auth_service.jwt.decode')
    async def test_verify_access_success(self, mock_decode: MagicMock) -> None:
        mock_decode.return_value = {"sub": str(self.user.uuid), "role": self.user.user_access.value}
        self.mock_user_service.get.return_value = ServiceResponse(
            status=status.HTTP_200_OK,
            message="Found",
            payload=self.user
        )
        token = "valid.token.here"
        response = await self.auth_service.verify_access(token, [UserAccess.ADMIN])
        self.assertEqual(response.status, status.HTTP_200_OK)
        self.assertEqual(response.payload.email, self.user.email)
        mock_decode.assert_called_once()

    @patch('api.services.auth_service.jwt.decode')
    async def test_verify_access_unauthorized_role(self, mock_decode: MagicMock) -> None:
        mock_decode.return_value = {"sub": str(self.user.uuid), "role": self.user.user_access.value}
        self.mock_user_service.get.return_value = ServiceResponse(
            status=status.HTTP_200_OK,
            message="Found",
            payload=self.user
        )
        response = await self.auth_service.verify_access("token", [UserAccess.GUEST])
        self.assertEqual(response.status, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("não possui o privilégio", response.message.lower())
        self.assertIsNone(response.payload)

    @patch('api.services.auth_service.jwt.decode')
    async def test_get_user_from_token_success(self, mock_decode: MagicMock) -> None:
        mock_decode.return_value = {"sub": str(self.user.uuid)}
        self.mock_user_service.get.return_value = ServiceResponse(
            status=status.HTTP_200_OK,
            message="Found",
            payload=self.user
        )
        user = await self.auth_service._get_user_from_token("token")
        self.assertEqual(user.email, self.user.email)

    @patch('api.services.auth_service.jwt.decode', side_effect=jwt.JWTError("Invalid token"))
    async def test_get_user_from_token_jwt_error(self, mock_decode: MagicMock) -> None:
        with self.assertRaises(HTTPException) as context:
            await self.auth_service._get_user_from_token("invalid.token")
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('api.services.auth_service.jwt.decode', side_effect=jwt.ExpiredSignatureError("Expired"))
    async def test_get_user_from_token_expired(self, mock_decode: MagicMock) -> None:
        with self.assertRaises(HTTPException) as context:
            await self.auth_service._get_user_from_token("expired.token")
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_access_token(self) -> None:
        data = {'sub': str(self.user.uuid), 'role': self.user.user_access.value}
        token = self.auth_service._create_access_token(data)
        self.assertIsInstance(token, str)
