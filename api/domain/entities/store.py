from datetime import date
from api.domain.entities.address import Address
from api.domain.entities.base_entity import BaseEntity
from api.enums.store_type import StoreType
from api.shared.validator import Validator
from api.domain.entities.user import User
from typing import List


class Store(BaseEntity):

    def __init__(self,
                cnpj: str,
                address: Address,
                reputation: float,
                trade_name: str,
                legal_name: str,
                owner: User,
                legal_phone_contact: str,
                preferred_phone_contact: str,
                legal_email_contact: str,
                preferred_email_contact: str,
                store_type: StoreType,
                opening_date: date,
                size: str,
                legal_nature: str,
                cnae_code: str,
                branch_classification: str,
                images: List[str] = [],
                **kwargs):
        super().__init__(**kwargs)
        self.images: List[str] = images
        self.cnpj: str = cnpj
        self.address: Address = address
        self.reputation: float = reputation
        self.trade_name: str = trade_name
        self.legal_name: str = legal_name
        self.owner: User = owner
        self.legal_phone_contact: str = legal_phone_contact
        self.preferred_phone_contact: str = preferred_phone_contact
        self.legal_email_contact: str = legal_email_contact
        self.preferred_email_contact: str = preferred_email_contact
        self.store_type: StoreType = store_type
        self.opening_date: date = opening_date
        self.size: str = size
        self.legal_nature: str = legal_nature
        self.cnae_code: str = cnae_code
        self.branch_classification: str = branch_classification