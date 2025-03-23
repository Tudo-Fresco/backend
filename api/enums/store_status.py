from enum import Enum


class StoreStatus(Enum):
    OPENED = 'OPENED'
    OUT_OF_BUSINESS = 'OUT_OF_BUSINESS'
    CLOSED = 'CLOSED'
    UNKNOWN = 'UNKNOWN'