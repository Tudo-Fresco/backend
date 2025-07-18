from sqlalchemy import Column, Enum, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.enums.demand_status import DemandStatus
from api.infrastructure.models.base_model import BaseModel
from api.domain.entities.demand import Demand
from api.infrastructure.models.product_model import ProductModel
from api.infrastructure.models.store_model import StoreModel
from api.infrastructure.models.user_model import UserModel
from sqlalchemy.orm import Mapped


class DemandModel(BaseModel):
    __tablename__ = 'demand'

    store_uuid = Column(UUID(as_uuid=True), ForeignKey('store.uuid'), nullable=False)
    product_uuid = Column(UUID(as_uuid=True), ForeignKey('product.uuid'), nullable=False)
    responsible_uuid = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), nullable=False)
    needed_count = Column(Integer, nullable=False)
    description = Column(String(512), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(DemandStatus), nullable=False, default=DemandStatus.OPENED)
    minimum_count = Column(Integer, nullable=False, default=1)

    store: Mapped[StoreModel] = relationship('StoreModel')
    product: Mapped[ProductModel] = relationship('ProductModel')
    responsible: Mapped[UserModel] = relationship('UserModel')

    def _from_entity(self, entity: Demand) -> None:
        '''Convert a Demand entity to the DemandModel.'''
        self.store_uuid = entity.store.uuid
        self.product_uuid = entity.product.uuid
        self.responsible_uuid = entity.responsible.uuid
        self.needed_count = entity.needed_count
        self.description = entity.description
        self.deadline = entity.deadline
        self.status = entity.status
        self.minimum_count = entity.minimum_count

    def _to_entity(self) -> Demand:
        '''Convert the DemandModel to a Demand entity.'''
        return Demand(
            store=self.store.to_entity(),
            product=self.product.to_entity(),
            responsible=self.responsible.to_entity(),
            needed_count=self.needed_count,
            description=self.description,
            deadline=self.deadline,
            status=self.status,
            minimum_count = self.minimum_count 
        )