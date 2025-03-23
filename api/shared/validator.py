from api.exceptions.validation_exception import ValidationException
from validate_docbr import CNPJ, CPF


class Validator:

    def __init__(self):
        self.current_field_errors = []

    def on(self, value: str, field_name: str):
        '''
        Starts a new validation process for the given value.
        '''
        self.value = value
        self.field_name = field_name
        return self

    def character_limit(self, limit: int, message: str = None):
        if len(self.value) > limit:
            self.current_field_errors.append(message or f'Value must be smaller than {limit} characters.')
        return self

    def not_empty(self, message: str = None):
        if not self.value:
            self.current_field_errors.append(message or 'Value cannot be empty.')
        return self

    def greater_or_equal(self, limit: float, message: str = None):
        if self.value <= limit:
            self.current_field_errors.append(message or f'Value must be greater or equal than {limit}')
        return self

    def smaller_or_equal(self, limit: float, message: str = None):
        if self.value >= limit:
            self.current_field_errors.append(message or f'Value must be smaller or equal than {limit}')
        return self

    def positive(self, message: str = None):
        if self.value <= 0:
            self.current_field_errors.append(message or 'Value must be a positive number')
        return self


    def cnpj_is_valid(self, message: str = None):
        cnpj = CNPJ()
        if not cnpj.validate(self.value):
            self.current_field_errors.append(message or f'{self.value} is not a valid Cnpj')
        return self
    
    def cpf_is_valid(self, message: str = None):
        cpf = CPF()
        if not cpf.validate(self.value):
            self.current_field_errors.append(message or f'{self.value} is not a valid Cpf')
        return self

    def with_message(self, message: str):
        '''
        Overrides the most recent error message.
        '''
        if self.current_field_errors:
            self.current_field_errors[-1] = message
        return self

    def check(self):
        '''
        Check all collected errors and raise a ValidationException if there are any errors.
        '''
        message: str = ''
        for error in self.current_field_errors:
            message = message.join(f'{self.field_name}: {error}\n')
        self.current_field_errors = []
        if message:
            raise ValidationException(message)
        return None
