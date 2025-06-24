import unittest
from datetime import date
from api.infrastructure.models.user_model import UserModel
from api.domain.entities.user import User
from api.enums.gender_type import GenderType
from api.enums.user_access import UserAccess
from api.enums.user_verification_status import UserVerificationStatus

class TestUserModel(unittest.TestCase):

    def setUp(self) -> None:
        self.user_entity = User(
            name="Test User",
            email="test@example.com",
            date_of_birth=date(1990, 1, 1),
            gender=GenderType.MALE,
            phone_number="+5511999999999",
            password="P@ssw0rd!!",
            user_access=UserAccess.ADMIN,
            profile_picture="profile.png",
            verification_status=UserVerificationStatus.EMAIL
        )

    def test_from_entity_populates_model_fields(self) -> None:
        model = UserModel()
        model._from_entity(self.user_entity)

        self.assertEqual(model.name, self.user_entity.name)
        self.assertEqual(model.email, self.user_entity.email)
        self.assertEqual(model.date_of_birth, self.user_entity.date_of_birth)
        self.assertEqual(model.gender, self.user_entity.gender)
        self.assertEqual(model.phone_number, self.user_entity.phone_number)
        self.assertEqual(model.profile_picture, self.user_entity.profile_picture)
        self.assertEqual(model.password, self.user_entity.password)
        self.assertEqual(model.user_access, self.user_entity.user_access)
        self.assertEqual(model.verification_status, self.user_entity.verification_status)

    def test_to_entity_returns_user_with_correct_fields(self) -> None:
        model = UserModel()
        model.name = "Test User"
        model.email = "test@example.com"
        model.date_of_birth = date(1990, 1, 1)
        model.gender = GenderType.MALE
        model.phone_number = "+5511999999999"
        model.profile_picture = "profile.png"
        model.password = "P@ssw0rd!!"
        model.user_access = UserAccess.ADMIN
        model.verification_status = UserVerificationStatus.EMAIL_AND_PHONE
        entity = model._to_entity()
        self.assertEqual(entity.name, model.name)
        self.assertEqual(entity.email, model.email)
        self.assertEqual(entity.date_of_birth, model.date_of_birth)
        self.assertEqual(entity.gender, model.gender)
        self.assertEqual(entity.phone_number, model.phone_number)
        self.assertEqual(entity.profile_picture, model.profile_picture)
        self.assertEqual(entity.password, model.password)
        self.assertEqual(entity.user_access, model.user_access)
        self.assertEqual(entity.verification_status, model.verification_status)