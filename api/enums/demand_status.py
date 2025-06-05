from enum import Enum


class DemandStatus(Enum):
    OPENED = 'OPENED'
    CLOSED = 'CLOSED'
    CANCELED = 'CANCELED'
    ANY = 'ANY'