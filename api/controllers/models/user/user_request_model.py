from datetime import date
from pydantic import EmailStr, Field
from api.controllers.models.base_request_model import BaseResquestModel
from api.enums.gender_type import GenderType


class UserRequestModel(BaseResquestModel):
    name: str = Field(..., example='Gabriel Voltolini')
    email: EmailStr = Field(..., example='gabriel@example.com')
    date_of_birth: date = Field(..., example='2000-01-01')
    gender: GenderType = Field(..., example=GenderType.MALE.value)
    phone_number: str = Field(..., example='+55 47 99999-9999')
    profile_picture: str = Field(..., example='https://example.com/profile.jpg')
    password: str = Field(..., example='securepassword123')