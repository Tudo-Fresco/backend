from urllib.parse import urlparse
from api.exceptions.validation_exception import ValidationException
from validate_docbr import CNPJ, CPF
from typing import Any


class Validator:

    def __init__(self):
        self.current_field_errors = []

    def on(self, value: Any, field_name: str):
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
        if self.value < limit:
            self.current_field_errors.append(message or f'Value must be greater or equal than {limit}')
        return self

    def greater(self, limit: float, message: str = None):
        if self.value <= limit:
            self.current_field_errors.append(message or f'Value must be greater than {limit}')
        return self

    def smaller_or_equal(self, limit: float, message: str = None):
        if self.value > limit:
            self.current_field_errors.append(message or f'Value must be smaller or equal than {limit}')
        return self

    def smaller(self, limit: float, message: str = None):
        if self.value >= limit:
            self.current_field_errors.append(message or f'Value must be smaller than {limit}')
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

    def url_is_valid(self, message: str = None):
            """Check if value is a syntactically valid URL."""
            is_string = isinstance(self.value, str)
            if not is_string:
                default_msg = 'URL must be a string'
                self.current_field_errors.append(message or default_msg)
                return self
            stripped_url = self.value.strip()
            is_empty = not stripped_url
            if is_empty:
                default_msg = 'URL cannot be empty'
                self.current_field_errors.append(message or default_msg)
                return self
            parsed_url = urlparse(self.value)
            has_scheme = bool(parsed_url.scheme)
            if not has_scheme:
                default_msg = 'URL must have a scheme (e.g., http:// or https://)'
                self.current_field_errors.append(message or default_msg)
                return self
            has_netloc = bool(parsed_url.netloc)
            if not has_netloc:
                default_msg = 'URL must have a domain (e.g., example.com)'
                self.current_field_errors.append(message or default_msg)
                return self
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
