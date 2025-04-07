from typing import List
from pydantic import Field
from api.controllers.models.base_response_model import BaseResponseModel
from api.enums.product_type import ProductType
from api.enums.unit_type import UnitType


class ProductResponseModel(BaseResponseModel):
    name: str = Field(..., example='Arroz Orgânico')
    unit_type: UnitType = Field(..., example='KILOGRAM')
    type: ProductType = Field(..., example=ProductType.GRAIN)
    images: List[str] = Field(..., example=['https://example.com/image1.jpg'])
    search_name: str = Field(..., example='arroz organico')
