from typing import List
from pydantic import Field
from api.controllers.models.base_request_model import BaseRequestModel
from api.enums.product_type import ProductType
from api.enums.unit_type import UnitType


class ProductRequestModel(BaseRequestModel):
    name: str = Field(..., max_length=256, example='Arroz Orgânico')
    unit_type: UnitType = Field(..., example='KILOGRAM')
    type: ProductType = Field(..., example=ProductType.GRAIN.value)
    images: List[str] = Field(default_factory=list, example=['https://example.com/image1.jpg'])
