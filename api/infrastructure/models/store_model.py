from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from api.domain.entities.store import Store
from api.infrastructure.models.address_model import AddressModel
from api.infrastructure.models.base_model import BaseModel
from api.infrastructure.models.user_model import UserModel


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

    owner: UserModel = relationship('UserModel', back_populates='stores')
    address: AddressModel = relationship('AddressModel', back_populates='stores')

    def from_entity(self, entity: Store) -> None:
        """Convert a Store entity to the StoreModel."""
        self.uuid = entity.uuid
        self.images = entity.images
        self.cnpj = entity.cnpj
        self.address_uuid = entity.address.uuid
        self.reputation = entity.reputation
        self.trade_name = entity.trade_name
        self.legal_name = entity.legal_name
        self.owner_uuid = entity.owner.uuid
        self.legal_phone_contact = entity.legal_phone_contact
        self.preferred_phone_contact = entity.preferred_phone_contact
        self.legal_email_contact = entity.legal_email_contact
        self.preferred_email_contact = entity.preferred_email_contact
        self.address = entity.address
        self.owner = UserModel().from_entity(entity.owner)

    def to_entity(self) -> Store:
        """Convert the StoreModel to a Store entity."""
        return Store(
            uuid=self.uuid,
            images=self.images,
            cnpj=self.cnpj,
            address=self.address.to_entity(),
            reputation=self.reputation,
            trade_name=self.trade_name,
            legal_name=self.legal_name,
            owner=self.owner.to_entity(),
            legal_phone_contact=self.legal_phone_contact,
            preferred_phone_contact=self.preferred_phone_contact,
            legal_email_contact=self.legal_email_contact,
            preferred_email_contact=self.preferred_email_contact
        )