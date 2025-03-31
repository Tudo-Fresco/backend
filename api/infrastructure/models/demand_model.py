from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.domain.entities.demand import Demand
from api.infrastructure.models.base_model import BaseModel
from api.infrastructure.models.product_model import ProductModel
from api.infrastructure.models.store_model import StoreModel
from api.infrastructure.models.user_model import UserModel


class DemandModel(BaseModel):
    __tablename__ = 'demand'

    store_uuid = Column(UUID(as_uuid=True), ForeignKey('store.uuid'), nullable=False)
    product_uuid = Column(UUID(as_uuid=True), ForeignKey('product.uuid'), nullable=False)
    responsible_uuid = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), nullable=False)
    needed_count = Column(Integer, nullable=False)
    description = Column(String(512), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)

    store: StoreModel = relationship('StoreModel', back_populates='demands')
    product: ProductModel = relationship('ProductModel', back_populates='demands')
    responsible: UserModel = relationship('UserModel', back_populates='demands')

    def from_entity(self, entity: Demand) -> None:
        """Convert a Demand entity to the DemandModel."""
        self.uuid = entity.uuid
        self.store_uuid = entity.store.uuid
        self.product_uuid = entity.product.uuid
        self.responsible_uuid = entity.responsible.uuid
        self.needed_count = entity.needed_count
        self.description = entity.description
        self.deadline = entity.deadline
        self.store = StoreModel()
        self.store.from_entity(entity.store)
        self.product = ProductModel()
        self.product.from_entity(entity.product)
        self.responsible = UserModel()
        self.responsible.from_entity(entity.responsible)

    def to_entity(self) -> Demand:
        """Convert the DemandModel to a Demand entity."""
        return Demand(
            uuid=self.uuid,
            store=self.store.to_entity(),
            product=self.product.to_entity(),
            responsible=self.responsible.to_entity(),
            needed_count=self.needed_count,
            description=self.description,
            deadline=self.deadline
        )
