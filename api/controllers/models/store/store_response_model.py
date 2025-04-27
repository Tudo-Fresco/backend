from datetime import date
from pydantic import EmailStr, Field
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.controllers.models.base_response_model import BaseResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from typing import List, Optional

from api.enums.store_type import StoreType


class StoreResponseModel(BaseResponseModel):
    images: Optional[List[str]] = Field(None, example=['https://example.com/image1.png'])
    cnpj: Optional[str] = Field(None, example='12.345.678/0001-99')
    address: Optional[AddressResponseModel]
    reputation: Optional[float] = Field(None, ge=0, le=5, example=4.7)
    trade_name: Optional[str] = Field(None, example='Loja Orgânica')
    legal_name: Optional[str] = Field(None, example='Loja Orgânica Ltda')
    owner: Optional[UserResponseModel]
    legal_phone_contact: Optional[str] = Field(None, example='(11) 1234-5678')
    preferred_phone_contact: Optional[str] = Field(None, example='(11) 98765-4321')
    legal_email_contact: Optional[EmailStr] = Field(None, example='legal@loja.com.br')
    preferred_email_contact: Optional[EmailStr] = Field(None, example='contato@loja.com.br')
    store_type: Optional[StoreType] = Field(None, example=StoreType.SUPPLIER.value)
    opening_date: Optional[date] = Field(None, example='2000-01-01')
    size: Optional[str] = Field(None, example='MICRO EMPRESA', description='Porte da empresa')
    legal_nature: Optional[str] = Field(None, example='206-2 - Sociedade Empresária Limitada', description='Natureza jurídica')
    cnae_code: Optional[str] = Field(None, example='62.01-5-01', description='Classificação Nacional de Atividades Econômicas')
    branch_classification: Optional[str] = Field(None, example='MATRIZ', description='Tipo')