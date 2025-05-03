from api.exceptions.validation_exception import ValidationException
from brazilnum.cnpj import validate_cnpj
from datetime import date
from typing import Any
import re


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
    
    def character_minimum(self, minimum: int, message: str = None):
        if len(self.value) < minimum:
            self._add_error(message or f'Value must be larger than {minimum} characters.')
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

    def cnpj_is_valid(self, message: str = None):
        if not isinstance(self.value, str):
            self._add_error(message or 'CNPJ must be a string.')
            return self
        if not validate_cnpj(self.value):
            self._add_error(message or f'{self.value} is not a valid CNPJ.')
            return self

        return self

    def is_adult(self, message: str = None):
        """
        Validates if the is 18 or older and not over 120.
        Assumes self.value is a datetime.date object.

        Args:
            message (str): Custom error message (optional)
        """
        today = date.today()
        age = today.year - self.value.year - ((today.month, today.day) < (self.value.month, self.value.day))
        if age < 18:
            self._add_error(message or 'Must be at least 18 years old.')
        elif age > 120:
            self._add_error(message or 'Age cannot exceed 120 years.')
        return self

    def phone_is_valid(self, message: str = None):
        phone_regex = r'^\(\d{2}\)\s(\d{4,5})-\d{4}$'
        if not re.match(phone_regex, self.value):
            self._add_error(message or f'{self.value} is not a valid phone number.')
        return self
        
    def has_minimum_special_characters(self, n: int, message: str = None):
        """
        Validates if the string contains exactly n special characters.
        Special characters are defined as: !@#$%^&*()_+-=[]{}|;:,.<>?/~
        
        Args:
            n (int): Exact number of special characters required
            message (str): Custom error message (optional)
        """
        special_char_pattern = r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~]'
        special_chars = re.findall(special_char_pattern, self.value)
        special_char_count = len(special_chars)
        if special_char_count < n:
            self._add_error(message or f'Value must contain exactly {n} special character(s).')
        return self

    def has_minimum_numbers(self, n: int, message: str = None):
        """
        Validates if the string contains exactly n digits (0-9).
        
        Args:
            n (int): Exact number of digits required
            message (str): Custom error message (optional)
        """
        digit_pattern = r'\d'
        digits = re.findall(digit_pattern, self.value)
        digit_count = len(digits)
        if digit_count < n:
            self._add_error(message or f'Value must contain exactly {n} digit(s).')
        return self

    def cep_is_valid(self, message: str = None):
        """
        Validates if the value is a valid Brazilian ZIP code (CEP).
        Accepts formats like '12345-678' or '12345678'.
        """
        cep_regex = r'^\d{5}-?\d{3}$'
        if not isinstance(self.value, str) or not re.match(cep_regex, self.value):
            self._add_error(message or f'{self.value} não é um CEP válido.')
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
                message += f'{field_name}: {error}\n\n'
            self.current_field_errors = []
            raise ValidationException(message)
        return None