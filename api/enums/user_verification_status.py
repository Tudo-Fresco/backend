from enum import Enum


class UserVerificationStatus(Enum):
    PENDING = 'PENDING'
    EMAIL = 'EMAIL'
    PHONE = 'PHONE'
    EMAIL_AND_PHONE = 'EMAIL_AND_PHONE'