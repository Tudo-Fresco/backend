from enum import Enum


class UserType(Enum):
    SUPPLIER = 'SUPPLIER'
    BUYER = 'BUYER'
    MODERATOR = 'MODERATOR'