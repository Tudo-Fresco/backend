from api.domain.entities.base_entity import BaseEntity
from api.domain.entities.product import Product
from api.domain.entities.store import Store
from api.domain.entities.user import User
from datetime import datetime


class Demand(BaseEntity):

    def __init__(self, store: Store,
                product: Product,
                responsible: User,
                needed_count: int,
                description: str,
                deadline: datetime, 
                **kwargs):
        super().__init__(**kwargs)
        self.store: Store = store
        self.product: Product = product
        self.responsible: User = responsible
        self.needed_count: int = needed_count
        self.description: str = description
        self.deadline: datetime= deadline
        