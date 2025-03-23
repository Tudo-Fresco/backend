from enum import Enum


class UserType(Enum):
    BUYER = 'BUYER'
    SELLER = 'SELLER'
    MODERATOR = 'MODERATOR'