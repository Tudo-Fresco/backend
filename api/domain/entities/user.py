from api.enums.gender_type import GenderType
from api.domain.entities.base_entity import BaseEntity
from datetime import date


class User(BaseEntity):
    
    def __init__(self, name: str,
                email: str,
                date_of_birth: date,
                gender: GenderType,
                phone_number: str,
                profile_picture: str,
                password: str,
                **kwargs):
        super().__init__(**kwargs)
        self.name: str = name
        self.email: str = email
        self.date_of_birth: date = date_of_birth
        self.gender: GenderType = gender
        self.phone_number: str = phone_number
        self.profile_picture: str = profile_picture
        self.password: str = password