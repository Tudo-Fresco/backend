import re
from typing import Any

from api.exceptions.validation_exception import ValidationException


class Validator:

    def __init__(self):
        self.current_field_errors = []
        self.value = None
        self.field_name = None

    def on(self, value: Any, field_name: str):
        self.value = value
        self.field_name = field_name
        return self

    def _add_error(self, message: str):
        self.current_field_errors.append((self.field_name, message))

    def character_limit(self, limit: int, message: str = None):
        if len(self.value) > limit:
            self._add_error(message or f'Value must be smaller than {limit} characters.')
        return self

    def not_empty(self, message: str = None):
        if not self.value:
            self._add_error(message or 'Value cannot be empty.')
        return self

    def email_is_valid(self, message: str = None):
        email_regex = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        if not isinstance(self.value, str):
            self._add_error(message or 'Email must be a string.')
            return self
        if not re.match(email_regex, self.value):
            self._add_error(message or f'{self.value} is not a valid email address.')
        return self

    def with_message(self, message: str):
        if self.current_field_errors:
            field_name, _ = self.current_field_errors[-1]
            self.current_field_errors[-1] = (field_name, message)
        return self

    def check(self):
        if self.current_field_errors:
            message = ''
            for field_name, error in self.current_field_errors:
                message += f'{field_name}: {error}\n'
            self.current_field_errors = []
            raise ValidationException(message)
        return None
