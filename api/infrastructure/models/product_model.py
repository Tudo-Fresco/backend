from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import ARRAY
from api.infrastructure.models.base_model import BaseModel
from api.domain.entities.product import Product
from api.enums.unit_type import UnitType
from api.enums.product_type import ProductType


class ProductModel(BaseModel):
    __tablename__ = 'product'

    name = Column(String(256), nullable=False)
    unit_type = Column(Enum(UnitType), nullable=False)
    type = Column(Enum(ProductType), nullable=False)
    images = Column(ARRAY(String), nullable=False, default=[])
    search_name = Column(String, nullable=False, default='')

    def _from_entity(self, entity: Product) -> None:
        '''Convert a Product entity to the ProductModel.'''
        self.name = entity.name
        self.unit_type = entity.unit_type
        self.type = entity.type
        self.images = entity.images
        self.search_name = entity.search_name

    def _to_entity(self) -> Product:
        '''Convert the ProductModel to a Product entity.'''
        return Product(
            name=self.name,
            unit_type=self.unit_type,
            type=self.type,
            images=self.images,
            search_name=self.search_name
        )