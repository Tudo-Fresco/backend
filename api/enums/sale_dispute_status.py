from enum import Enum


class SaleDisputeStatus(Enum):
    SORTED = 'SORTED'
    PENDING = 'PENDING'
    WITHDRAWN = 'WITHDRAWN'
    REJECTED = 'REJECTED'