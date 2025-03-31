from api.domain.entities.product import Product
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

    def from_entity(self, entity: Product) -> None:
        """Convert a Product entity to the ProductModel."""
        self.uuid = entity.uuid
        self.name = entity.name
        self.unit_type = entity.unit_type
        self.type = entity.type
        self.images = entity.images
        self.search_name = entity.search_name

    def to_entity(self) -> Product:
        """Convert the ProductModel to a Product entity."""
        return Product(
            uuid=self.uuid,
            name=self.name,
            unit_type=self.unit_type,
            type=self.type,
            images=self.images,
            search_name=self.search_name
        )