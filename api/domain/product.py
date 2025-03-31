from api.domain.base_entity import BaseEntity
from api.enums.product_type import ProductType
from api.enums.unit_type import UnitType
from api.shared.validator import Validator
from typing import List


class Product(BaseEntity):

    def __init__(self, name: str,
                unit_type: UnitType,
                type: ProductType,
                images: List[str],
                search_name: str = '',
                **kwargs) -> None:
        super().__init__(**kwargs)
        self.name: str = name
        self.unit_type: UnitType = unit_type
        self.type: ProductType = type
        self.images: List[str] = images
        self.search_name: str = search_name

    def validate(self) -> None:
        validator = Validator()
        validator.on(self.name, 'Nome do produto').character_limit(256, 'Deve ser menor do que 256 caracteres.').check()