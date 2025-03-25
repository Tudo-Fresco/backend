from typing import Dict
from sqlalchemy import ARRAY, Column, String, Float, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from api.infrastructure.models.base_model import BaseModel
from api.domain.store import Store
from api.enums.store_status import StoreStatus


class StoreModel(BaseModel):
    __tablename__ = 'store'

    cnpj = Column(String, nullable=False)
    reputation = Column(Float, nullable=False)
    trade_name = Column(String, nullable=False)
    legal_name = Column(String, nullable=False)
    working_hours = Column(String, nullable=False)
    status = Column(Enum(StoreStatus), nullable=False)
    image_urls = Column(ARRAY(String), nullable=False, default=list)
    headquarters_id = Column(PG_UUID(as_uuid=True), ForeignKey('store.uuid'), nullable=True)
    address_id = Column(PG_UUID(as_uuid=True), ForeignKey('address.uuid'), nullable=False)
    group_id = Column(PG_UUID(as_uuid=True), ForeignKey('group.uuid'), nullable=False)
    owner_id = Column(PG_UUID(as_uuid=True), ForeignKey('user.uuid'), nullable=False)

    headquarters = relationship('StoreModel', remote_side='StoreModel.uuid', uselist=False, nullable=True)
    address = relationship('AddressModel', uselist=False)
    group = relationship('GroupModel', uselist=False)
    owner = relationship('UserModel', uselist=False)

    def __repr__(self):
        return f"<StoreModel(uuid={self.uuid}, trade_name={self.trade_name})>"

    def to_entity(self) -> Store:
        """Convert StoreModel to Store domain entity."""
        return Store(
            uuid=self.uuid,
            active=self.active,
            created_at=self.created_at,
            updated_at=self.updated_at,
            headquarters=self.headquarters.to_entity() if self.headquarters else None,
            image_urls=self.image_urls,
            cnpj=self.cnpj,
            address=self.address.to_entity(),
            status=self.status,
            reputation=self.reputation,
            trade_name=self.trade_name,
            legal_name=self.legal_name,
            group=self.group.to_entity(),
            working_hours=self.working_hours,
            owner=self.owner.to_entity()
        )