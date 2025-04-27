from datetime import date
from pydantic import EmailStr, Field
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.controllers.models.base_response_model import BaseResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from typing import List

from api.enums.store_type import StoreType


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
    store_type: StoreType = Field(..., example=StoreType.SUPPLIER.value)
    opening_date: date = Field(..., example='2000-01-01')
    size: str = Field(..., example='MICRO EMPRESA', description='Porte da empresa')
    legal_nature: str = Field(..., example='206-2 - Sociedade Empresária Limitada', description='Natureza jurídica')
    cnae_code: str = Field(..., example='62.01-5-01', description='Classificação Nacional de Atividades Econômicas')
    branch_classification: str = Field(..., example='MATRIZ', description='Tipo')