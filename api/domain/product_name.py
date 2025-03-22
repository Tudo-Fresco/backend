from api.domain.base_entity import BaseEntity
from api.shared.validator import Validator

class ProductName(BaseEntity):

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name

    def validate(self) -> None:
        validator = Validator()
        validator.validate(self.name, 'Nome do produto').character_limit(256, 'Deve ser menor do que 256 caracteres.').check()