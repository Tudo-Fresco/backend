from api.enums.user_verification_status import UserVerificationStatus
from api.shared.password_hasher import PasswordHasher
from api.domain.entities.base_entity import BaseEntity
from api.enums.gender_type import GenderType
from api.enums.user_access import UserAccess
from datetime import date

from api.shared.validator import Validator


class User(BaseEntity):
    
    def __init__(self, name: str,
                email: str,
                date_of_birth: date,
                gender: GenderType,
                phone_number: str,
                password: str,
                user_access: UserAccess,
                profile_picture: str = '',
                verification_status: UserVerificationStatus = UserVerificationStatus.PENDING,
                **kwargs):
        super().__init__(**kwargs)
        self.name: str = name
        self.email: str = email
        self.date_of_birth: date = date_of_birth
        self.gender: GenderType = gender
        self.phone_number: str = phone_number
        self.password: str = password
        self.user_access: UserAccess = user_access
        self.profile_picture: str = profile_picture
        self.verification_status: UserVerificationStatus = verification_status

    def hash_password(self) -> None:
        self.password: str = PasswordHasher.hash(self.password)
    
    def validate(self):
        validator = Validator()
        validator.on(self.email, 'E-mail').email_is_valid(f'{self.email} é inválido')
        validator.on(self.date_of_birth, 'Data de nascimento').is_adult('o usuário deve ser maior de 18 anos')
        validator.on(self.phone_number, 'Número de telefone').phone_is_valid(f'{self.phone_number} é inválido')
        validator.on(self.password, 'Senha').has_minimum_special_characters(2, 'deve conter pelo menos 2 caracteres especiais')
        validator.on(self.password, 'Senha').has_minimum_numbers(2, 'deve conter pelo menos 2 números')
        validator.on(self.password, 'Senha').character_limit(32, 'deve ser menor do que 32 caracteres')
        validator.on(self.password, 'Senha').character_minimum(4, 'deve ser maior do que 4 caracteres')
        validator.check()