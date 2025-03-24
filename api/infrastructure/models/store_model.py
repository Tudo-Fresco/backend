from api.enums.store_status import StoreStatus
from sqlalchemy import ARRAY, Column, String, Float, Enum, ForeignKey
from api.infrastructure.models.base_model import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class StoreModel(BaseModel):
    __tablename__ = 'stores'
    cnpj = Column(String, nullable=False)
    reputation = Column(Float, nullable=False)
    trade_name = Column(String, nullable=False)
    legal_name = Column(String, nullable=False)
    working_hours = Column(String, nullable=False)
    status = Column(Enum(StoreStatus), nullable=False)
    image_urls = Column(ARRAY(String), nullable=False, default=list)  
    headquarters_id = Column(UUID(as_uuid=True), ForeignKey('stores.uuid'), nullable=True)
    address_id = Column(UUID(as_uuid=True), ForeignKey('addresses.uuid'), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.uuid'), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False)
    headquarters = relationship('StoreModel', remote_side='StoreModel.uuid', uselist=False, nullable=True)
    address = relationship('AddressModel', uselist=False)
    group = relationship('GroupModel', uselist=False)
    owner = relationship('UserModel', uselist=False)

    def __repr__(self):
        return f"<StoreModel(uuid={self.uuid}, trade_name={self.trade_name})>"
