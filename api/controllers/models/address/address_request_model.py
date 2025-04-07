from pydantic import Field
from api.controllers.models.base_request_model import BaseResquestModel


class AddressRequestModel(BaseResquestModel):
    zip_code: str = Field(..., example='12345-678')
    street_address: str = Field(..., example='Av. Paulista')
    latitude: float = Field(..., example=-23.561684)
    longitude: float = Field(..., example=-46.655981)
    province: str = Field(..., example='São Paulo')
    city: str = Field(..., example='São Paulo')
    neighbourhood: str = Field(..., example='Bela Vista')
    number: str = Field(..., example='1000')
    additional_info: str = Field(default='', example='Apt 101')
