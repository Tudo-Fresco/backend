from pydantic import EmailStr, Field
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.controllers.models.base_response_model import BaseResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from typing import List


class StoreResponseModel(BaseResponseModel):
    images: List[str] = Field(..., example=['https://example.com/image1.png'])
    cnpj: str = Field(..., example='12.345.678/0001-99')
    address: AddressResponseModel
    reputation: float = Field(..., ge=0, le=5, example=4.7)
    trade_name: str = Field(..., example='Loja Orgânica')
    legal_name: str = Field(..., example='Loja Orgânica Ltda')
    owner: UserResponseModel
    legal_phone_contact: str = Field(..., example='(11) 1234-5678')
    preferred_phone_contact: str = Field(..., example='(11) 98765-4321')
    legal_email_contact: EmailStr = Field(..., example='legal@loja.com.br')
    preferred_email_contact: EmailStr = Field(..., example='contato@loja.com.br')
