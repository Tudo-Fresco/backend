from datetime import date
from pydantic import EmailStr, Field
from api.controllers.models.base_response_model import BaseResponseModel
from api.enums.gender_type import GenderType
from api.enums.user_access import UserAccess


class UserResponseModel(BaseResponseModel):
    name: str = Field(..., example='Gabriel Voltolini')
    email: EmailStr = Field(..., example='gabriel@example.com')
    date_of_birth: date = Field(..., example='2000-01-01')
    gender: GenderType = Field(..., example=GenderType.MALE.value)
    phone_number: str = Field(..., example='+55 47 99999-9999')
    profile_picture: str = Field(..., example='https://example.com/profile.jpg')
    user_access: UserAccess = Field(..., example=UserAccess.ADMIN)
