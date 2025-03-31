from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.infrastructure.models.base_model import BaseModel


class DemandModel(BaseModel):
    __tablename__ = 'demand'

    store_uuid = Column(UUID(as_uuid=True), ForeignKey('store.uuid'), nullable=False)
    product_uuid = Column(UUID(as_uuid=True), ForeignKey('product.uuid'), nullable=False)
    responsible_uuid = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), nullable=False)
    needed_count = Column(Integer, nullable=False)
    description = Column(String(512), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    store = relationship('StoreModel', back_populates='demands')
    product = relationship('ProductModel', back_populates='demands')
    responsible = relationship('UserModel', back_populates='demands')
