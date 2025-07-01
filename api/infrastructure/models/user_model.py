from sqlalchemy import Column, Date, Enum, String
from api.enums.user_access import UserAccess
from api.enums.user_verification_status import UserVerificationStatus
from api.infrastructure.models.base_model import BaseModel
from api.domain.entities.user import User
from api.enums.gender_type import GenderType


class UserModel(BaseModel):
    __tablename__ = 'user'

    name = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(GenderType), nullable=False)
    phone_number = Column(String(32), nullable=False)
    profile_picture = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_access = Column(Enum(UserAccess), nullable=False)
    verification_status = Column(Enum(UserVerificationStatus), nullable=True)


    def _from_entity(self, entity: User) -> None:
        '''Convert a User entity to the UserModel.'''
        self.name = entity.name
        self.email = entity.email
        self.date_of_birth = entity.date_of_birth
        self.gender = entity.gender
        self.phone_number = entity.phone_number
        self.profile_picture = entity.profile_picture
        self.password = entity.password
        self.user_access = entity.user_access
        self.verification_status = entity.verification_status

    def _to_entity(self) -> User:
        '''Convert the UserModel to a User entity.'''
        return User(
            name=self.name,
            email=self.email,
            date_of_birth=self.date_of_birth,
            gender=self.gender,
            phone_number=self.phone_number,
            profile_picture=self.profile_picture,
            password=self.password,
            user_access=self.user_access,
            verification_status = self.verification_status
        )