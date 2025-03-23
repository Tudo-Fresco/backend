from enum import Enum


class UserAccess(Enum):
    ADMIN = 'ADMIN'
    EDITOR = 'EDITOR'
    GUEST = 'GUEST'