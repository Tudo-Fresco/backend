from api.domain.base_entity import BaseEntity
from api.domain.certification import Certification
from api.domain.product_name import ProductName
from api.enums.product_type import ProductType
from api.domain.store import Store
from api.enums.unit_type import UnitType
from api.shared.validator import Validator


class Product(BaseEntity):

    def __init__(self, name: ProductName,
                type: ProductType,
                code: str,
                unit_cost: float,
                unit_price: float, 
                unit_type: UnitType,
                unit_stock_count: int,
                product_image_urls: list[str],
                store: Store,
                certification: Certification = None,
                **kwargs) -> None:
        super().__init__(**kwargs)
        self.name: ProductName = name
        self.type: ProductType = type
        self.code: str = code
        self.unit_cost: float = unit_cost
        self.unit_price: float = unit_price
        self.unit_type: UnitType = unit_type
        self.unit_stock_count: int = unit_stock_count
        self.product_image_urls: list[str] = product_image_urls
        self.store: Store = store
        self.certification: Certification = certification

    def validate(self) -> None:
        validator = Validator()
        validator.validate(self.code, 'Código do produto').character_limit(1024, 'Deve ser menor que 1024 caracteres.')
        validator.validate(self.unit_cost, 'Custo da unidade').be_posive('Deve ser um valor positivo')
        validator.validate(self.unit_price, 'Preço da unidade').greater_than_zero('Deve ser maior que 0')
        validator.validate(self.unit_stock_count, 'Quantidade no estoque').be_posive('Deve ser um valor positivo')
        validator.check()
        self.name.validate()
        self.store.validate()
        if self.certification:
            self.certification.validate()
    
    def calculate_price(self, units: int) -> float:
        price: float = units * self.unit_price
        return price

    def calculate_cost(self, units: int) -> float:
        cost: float = units * self.unit_cost
        return cost

    def calculate_profit(self, units: int) -> float:
        cost: float = self.calculate_cost(units)
        price: float = self.calculate_price(units)
        profit: float = price - cost
        return profit

    def sell(self, units: int) -> None:
        self.unit_stock_count -= units

    def restock(self, units: int) -> None:
        self.unit_stock_count += units