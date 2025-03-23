from api.domain.address import Address
from api.domain.base_entity import BaseEntity
from api.domain.group import Group
from api.shared.validator import Validator
from api.domain.user import User
from api.enums.store_status import StoreStatus
from typing import List, Optional


class Store(BaseEntity):

    def __init__(self, headquarters: Optional['Store'],
                image_urls: List[str],
                cnpj: str,
                address: Address,
                status: StoreStatus,
                reputation: float,
                trade_name: str,
                legal_name: str,
                group: Group,
                working_hours: str,
                owner: User,
                **kwargs):
        super().__init__(**kwargs)
        self.headquarters = headquarters
        self.image_urls = image_urls
        self.cnpj = cnpj
        self.address = address
        self.status = status
        self.reputation = reputation
        self.trade_name = trade_name
        self.legal_name = legal_name
        self.group = group
        self.working_hours = working_hours
        self.owner = owner

    def validate(self) -> None:
        validator = Validator()
        validator.on(self.cnpj, 'Cnpj').cnpj_is_valid(f'O cnpj {self.cnpj} é inválido.')
        validator.on(self.reputation, 'Reputação').greater_or_equal(0, 'Deve ser maior ou igual a 0')
        validator.on(self.reputation, 'Reputação').smaller_or_equal(5, 'Deve ser menor ou igual a 5')
        validator.on(self.trade_name, 'Nome Fantasia').not_empty('Não foi informado')
        validator.on(self.legal_name, 'Razão Social').not_empty('Não foi informado')
        validator.on(self.working_hours, 'Horário de Atendimento').not_empty('Não foi informado')
        validator.check()
        self.address.validate()
        self.group.validate()
        self.owner.validate()