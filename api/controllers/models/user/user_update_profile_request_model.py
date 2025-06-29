from datetime import date
from uuid import UUID
from pydantic import Field
from api.controllers.models.base_request_model import BaseRequestModel
from api.enums.gender_type import GenderType


class UserUpdateProfileRequestModel(BaseRequestModel):
    uuid: UUID = Field(..., example='123e4567-e89b-12d3-a456-426614174000')
    name: str = Field(..., example='Gabriel Voltolini')
    email: str = Field(..., example='gabriel@example.com')
    date_of_birth: date = Field(..., example='2000-01-01')
    gender: GenderType = Field(..., example=GenderType.MALE.value)
    phone_number: str = Field(..., example='+55 47 99999-9999')
    password: str = Field(example='new user password')
    current_password: str = Field(example='new user password')
