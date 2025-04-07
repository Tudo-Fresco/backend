from pydantic import EmailStr, Field
from api.controllers.models.address.address_request_model import AddressRequestModel
from api.controllers.models.base_request_model import BaseResquestModel
from api.controllers.models.user.user_request_model import UserRequestModel
from typing import List


class StoreRequestModel(BaseResquestModel):
    images: List[str] = Field(default_factory=list, example=['https://example.com/image1.png'])
    cnpj: str = Field(..., example='12.345.678/0001-99')
    address: AddressRequestModel
    reputation: float = Field(..., ge=0, le=5, example=4.7)
    trade_name: str = Field(..., example='Loja Orgânica')
    legal_name: str = Field(..., example='Loja Orgânica Ltda')
    owner: UserRequestModel
    legal_phone_contact: str = Field(..., example='(11) 1234-5678')
    preferred_phone_contact: str = Field(..., example='(11) 98765-4321')
    legal_email_contact: EmailStr = Field(..., example='legal@loja.com.br')
    preferred_email_contact: EmailStr = Field(..., example='contato@loja.com.br')