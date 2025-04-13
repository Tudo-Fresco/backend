from api.domain.entities.base_entity import BaseEntity
from api.enums.product_type import ProductType
from api.enums.unit_type import UnitType
from api.shared.validator import Validator
from typing import List


class Product(BaseEntity):

    UNIT_TYPE_ABBREVIATIONS = {
        UnitType.METRIC_TON: 't',
        UnitType.KILOGRAM: 'kg',
        UnitType.GRAM: 'g',
        UnitType.PIECE: 'uni.',
    }

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
        if not search_name:
            self.search_name = self._get_search_name()

    def validate(self) -> None:
        validator = Validator()
        validator.on(self.name, 'Nome do produto').character_limit(256, 'Deve ser menor do que 256 caracteres.').not_empty('É obrigatório')
        validator.check()

    def _get_search_name(self) -> str:
        unit = self._get_type_abbreviation(self.unit_type)
        return f"{self.name} ({unit})"
    
    def _get_type_abbreviation(self, unit_type: UnitType) -> str:
        try:
            return self.UNIT_TYPE_ABBREVIATIONS[unit_type]
        except KeyError:
            raise ValueError(f'Tipo de unidade desconhecido: {unit_type}')
    