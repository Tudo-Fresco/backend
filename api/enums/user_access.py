from enum import Enum


class UserAccess(Enum):
    ADMIN = 'ADMIN'
    STORE_OWNER = 'STORE_OWNER'
    EMPLOYEE = 'EMPLOYEE'
    GUEST = 'GUEST'
    ANY = 'ANY'