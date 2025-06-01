from sqlalchemy import Column, Date, Enum, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from api.enums.store_type import StoreType
from api.infrastructure.models.base_model import BaseModel
from api.domain.entities.store import Store
from api.infrastructure.models.address_model import AddressModel
from api.infrastructure.models.user_model import UserModel
from sqlalchemy.orm import Mapped


class StoreModel(BaseModel):
    __tablename__ = 'store'

    images = Column(ARRAY(String), nullable=False, default=[])
    cnpj = Column(String(18), nullable=False, unique=False)
    address_uuid = Column(UUID(as_uuid=True), ForeignKey('address.uuid'), nullable=False)
    reputation = Column(Float, nullable=False)
    trade_name = Column(String(256), nullable=False)
    legal_name = Column(String(256), nullable=False)
    owner_uuid = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), nullable=False)
    legal_phone_contact = Column(String(20), nullable=False)
    preferred_phone_contact = Column(String(20), nullable=False)
    legal_email_contact = Column(String(256), nullable=False)
    preferred_email_contact = Column(String(256), nullable=False)
    store_type = Column(Enum(StoreType), nullable=False)
    opening_date = Column(Date, nullable=False)
    size = Column(String(64), nullable=False)
    legal_nature = Column(String(64), nullable=False)
    cnae_code = Column(String(20), nullable=False)
    branch_classification = Column(String(64), nullable=False)

    address: Mapped[AddressModel] = relationship('AddressModel')
    owner: Mapped[UserModel]  = relationship('UserModel')

    def _from_entity(self, entity: Store) -> None:
        '''Convert a Store entity to the StoreModel.'''
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
        self.store_type = entity.store_type
        self.opening_date = entity.opening_date
        self.size = entity.size
        self.legal_nature = entity.legal_nature
        self.cnae_code = entity.cnae_code
        self.branch_classification = entity.branch_classification

    def _to_entity(self) -> Store:
        '''Convert the StoreModel to a Store entity.'''
        return Store(
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
            preferred_email_contact=self.preferred_email_contact,
            store_type=self.store_type,
            opening_date=self.opening_date,
            size=self.size,
            legal_nature=self.legal_nature,
            cnae_code=self.cnae_code,
            branch_classification=self.branch_classification
        )