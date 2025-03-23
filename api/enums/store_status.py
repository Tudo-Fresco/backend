from enum import Enum


class StoreStatus(Enum):
    ACTIVE = 'ACTIVE'
    OUT_OF_BUSINESS = 'OUT_OF_BUSINESS'
    CLOSED = 'CLOSED'
    UNKNOWN = 'UNKNOWN'