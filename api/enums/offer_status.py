from enum import Enum


class OfferStatus(Enum):
    DONE = 'DONE'
    OPEN = 'OPEN'
    CANCELLED = 'CANCELLED'