from api.domain.base_entity import BaseEntity
from api.shared.validator import Validator
from sqlalchemy import Column, String



class ProductName(BaseEntity):
    __tablename__ = 'product_name'

    name = Column(String, nullable=False)

    def validate(self) -> None:
        validator = Validator()
        validator.validate(self.name, 'Nome do produto').character_limit(256, 'Deve ser menor do que 256 caracters.').check()