from uuid import UUID
from typing import List
from pydantic import Field
from api.controllers.models.base_request_model import BaseRequestModel
from api.enums.store_type import StoreType


class StoreRequestModel(BaseRequestModel):
    cnpj: str = Field(..., example="12.345.678/0001-90", description="CNPJ da loja")
    trade_name: str = Field(..., example="Tudo Fresco Orgânicos", description="Nome fantasia da loja")
    legal_name: str = Field(..., example="Tudo Fresco Ltda", description="Razão social da loja")
    legal_phone_contact: str = Field(..., example="+55 11 4002-8922", description="Telefone jurídico de contato")
    preferred_phone_contact: str = Field(..., example="+55 11 98888-7777", description="Telefone preferencial de contato")
    legal_email_contact: str = Field(..., example="juridico@tudofresco.com.br", description="E-mail jurídico da loja")
    preferred_email_contact: str = Field(..., example="contato@tudofresco.com.br", description="E-mail preferencial da loja")
    images: List[str] = Field(default_factory=list, example=["https://image1.com", "https://image2.com"], description="Lista de URLs de imagens da loja")
    reputation: float = Field(0.0, example=4.5, description="Reputação da loja (de 0 a 5)")
    owner_uuid: UUID = Field(..., example="6a79c74a-5016-4f6f-ae9c-83d3c6a30851", description="UUID do proprietário da loja")
    address_uuid: UUID = Field(..., example="3ec37df2-2e6b-4b4a-9f25-60fd20ec0fd8", description="UUID do endereço da loja")
    store_type: StoreType = Field(..., example=StoreType.SUPPLIER.value)
