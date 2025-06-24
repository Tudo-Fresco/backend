import unittest
from unittest.mock import AsyncMock, MagicMock
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from api.controllers.user_controller import UserController
from api.enums.gender_type import GenderType
from api.enums.user_access import UserAccess
from api.services.service_response import ServiceResponse
from api.controllers.models.user.user_response_model import UserResponseModel
from api.controllers.models.user.user_request_model import UserRequestModel
from api.controllers.models.user.user_update_profile_request_model import UserUpdateProfileRequestModel


class TestUserController(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.mock_service = MagicMock()
        self.mock_auth_wrapper = MagicMock()
        self.controller = UserController(service=self.mock_service, auth_wrapper=self.mock_auth_wrapper)

        self.user = UserResponseModel(
            uuid="12345678-1234-5678-1234-567812345678",
            name="Gabriel Voltolini",
            email="gabriel@example.com",
            date_of_birth="2000-01-01",
            gender="MALE",
            phone_number="+55 47 99999-9999",
            profile_picture="https://example.com/profile.jpg",
            user_access=UserAccess.ANY,
            verification_status="EMAIL_AND_PHONE"
        )

    def test_routes_and_auth_wrapper_setup(self) -> None:
        expected_roles_sets = [
            {UserAccess.EMPLOYEE, UserAccess.STORE_OWNER, UserAccess.ADMIN},
            {UserAccess.ANY}
        ]
        for call_args in self.mock_auth_wrapper.with_access.call_args_list:
            actual_roles = set(call_args.args[0])
            self.assertTrue(
                any(expected.issubset(actual_roles) for expected in expected_roles_sets),
                f"Unexpected roles passed to with_access: {actual_roles}"
            )

    async def test_sign_up_handler_success(self) -> None:
        self.mock_service.sign_up = AsyncMock(return_value=ServiceResponse(
            status=201,
            message="User created",
            payload={"uuid": "some-uuid"}
        ))

        endpoint = self.controller._sign_up_handler()
        model = UserRequestModel(
            name="New User",
            email="newuser@example.com",
            date_of_birth="1990-01-01",
            gender=GenderType.MALE,
            phone_number="+55 11 99999-9999",
            profile_picture="https://example.com/pic.jpg",
            user_access=UserAccess.ANY,
            password='abc123^'
        )
        response = await endpoint(model=model)
        self.mock_service.sign_up.assert_awaited_once_with(request=model)
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created", response.body.decode())

    async def test_upload_profile_picture_handler_success(self) -> None:
        self.mock_service.upload_profile_picture = AsyncMock(return_value=ServiceResponse(
            status=200,
            message="Profile picture uploaded",
            payload={"url": "https://example.com/image.jpg"}
        ))

        endpoint = self.controller._upload_profile_picture_handler()
        mock_file = MagicMock(spec=UploadFile)
        mock_file.read = AsyncMock(return_value=b"fake-image-bytes")
        mock_file.filename = "profile.jpg"

        response = await endpoint(file=mock_file, user=self.user)

        self.mock_service.upload_profile_picture.assert_awaited_once_with(
            user_uuid=self.user.uuid,
            image_bytes=b"fake-image-bytes",
            file_name="profile.jpg"
        )
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Profile picture uploaded", response.body.decode())

    async def test_get_signed_profile_image_url_handler_success(self) -> None:
        self.mock_service.get_profile_image_signed_url = AsyncMock(return_value=ServiceResponse(
            status=200,
            message="Signed URL generated",
            payload={"url": "https://signed-url.com/image.jpg"}
        ))

        endpoint = self.controller._get_signed_profile_image_url_handler()
        response = await endpoint(user=self.user)
        self.mock_service.get_profile_image_signed_url.assert_awaited_once_with(self.user.uuid)
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Signed URL generated", response.body.decode())

    async def test_update_profile_handler_success(self) -> None:
        self.mock_service.update_profile = AsyncMock(return_value=ServiceResponse(
            status=200,
            message="Profile updated",
            payload=self.user
        ))
        user_update_dict: dict = {"current_password": "password123#", "password": "password123#%"}
        user_update_dict.update(self.user.model_dump())
        endpoint = self.controller._update_profile_handler()
        update_request = UserUpdateProfileRequestModel(**user_update_dict)
        response = await endpoint(request=update_request, user=self.user)
        self.mock_service.update_profile.assert_awaited_once_with(self.user, update_request)
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Profile updated", response.body.decode())
