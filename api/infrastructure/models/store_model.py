from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from api.infrastructure.models.base_model import BaseModel


class StoreModel(BaseModel):
    __tablename__ = 'store'

    images = Column(ARRAY(String), nullable=False, default=[])
    cnpj = Column(String(18), nullable=False, unique=True)
    address_uuid = Column(UUID(as_uuid=True), ForeignKey('address.uuid'), nullable=False)
    reputation = Column(Float, nullable=False)
    trade_name = Column(String(256), nullable=False)
    legal_name = Column(String(256), nullable=False)
    owner_uuid = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), nullable=False)
    legal_phone_contact = Column(String(20), nullable=False)
    preferred_phone_contact = Column(String(20), nullable=False)
    legal_email_contact = Column(String(256), nullable=False)
    preferred_email_contact = Column(String(256), nullable=False)

    owner = relationship('UserModel', back_populates='stores')
    address = relationship('AddressModel', back_populates='stores')
