from api.infrastructure.models.base_model import BaseModel
from sqlalchemy import Column, String, Enum, ARRAY
from api.enums.product_type import ProductType
from api.enums.unit_type import UnitType


class ProductModel(BaseModel):
    __tablename__ = 'product'

    name = Column(String(256), nullable=False)
    unit_type = Column(Enum(UnitType), nullable=False)
    type = Column(Enum(ProductType), nullable=False)
    images = Column(ARRAY(String), nullable=False, default=[])
    search_name = Column(String, nullable=False, default='')
