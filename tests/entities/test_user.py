import unittest
from datetime import date
from unittest.mock import patch, MagicMock
from api.domain.entities.user import User
from api.enums.gender_type import GenderType
from api.enums.user_access import UserAccess
from api.enums.user_verification_status import UserVerificationStatus


class TestUser(unittest.TestCase):

    def setUp(self) -> None:
        self.user_kwargs = {
            "name": "Test User",
            "email": "test@example.com",
            "date_of_birth": date(1990, 1, 1),
            "gender": GenderType.MALE,
            "phone_number": "+5511999999999",
            "password": "P@ssw0rd12",
            "user_access": UserAccess.ADMIN,
            "profile_picture": "",
            "verification_status": UserVerificationStatus.PENDING,
        }

    def test_init_sets_all_properties(self) -> None:
        user = User(**self.user_kwargs)
        self.assertEqual(user.name, self.user_kwargs['name'])
        self.assertEqual(user.email, self.user_kwargs['email'])
        self.assertEqual(user.date_of_birth, self.user_kwargs['date_of_birth'])
        self.assertEqual(user.gender, self.user_kwargs['gender'])
        self.assertEqual(user.phone_number, self.user_kwargs['phone_number'])
        self.assertEqual(user.password, self.user_kwargs['password'])
        self.assertEqual(user.user_access, self.user_kwargs['user_access'])
        self.assertEqual(user.profile_picture, self.user_kwargs['profile_picture'])
        self.assertEqual(user.verification_status, self.user_kwargs['verification_status'])

    @patch('api.shared.password_hasher.PasswordHasher.hash')
    def test_hash_password_calls_password_hasher(self, mock_hash) -> None:
        mock_hash.return_value = 'hashed_password'
        user = User(**self.user_kwargs)
        user.hash_password()
        mock_hash.assert_called_once_with(self.user_kwargs['password'])
        self.assertEqual(user.password, 'hashed_password')

    @patch('api.domain.entities.user.Validator')
    def test_validate_calls_validator_methods(self, mock_validator_cls) -> None:
        mock_validator = MagicMock()
        mock_validator.check = MagicMock()
        mock_validator_cls.return_value = mock_validator
        user = User(**self.user_kwargs)
        user.validate()
        self.assertEqual(mock_validator.on.call_count, 7)
        mock_validator.check.assert_called_once()