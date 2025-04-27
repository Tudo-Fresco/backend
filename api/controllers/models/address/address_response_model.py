from typing import Optional
from pydantic import Field
from api.controllers.models.base_response_model import BaseResponseModel


class AddressResponseModel(BaseResponseModel):
    zip_code: Optional[str] = Field(None, example='12345-678')
    street_address: Optional[str] = Field(None, example='Av. Paulista')
    latitude: Optional[float] = Field(None, example=-23.561684)
    longitude: Optional[float] = Field(None, example=-46.655981)
    province: Optional[str] = Field(None, example='São Paulo')
    city: Optional[str] = Field(None, example='São Paulo')
    neighbourhood: Optional[str] = Field(None, example='Bela Vista')
    number: Optional[str] = Field(None, example='1000')
    additional_info: Optional[str] = Field(default=None, example='Apt 101')
