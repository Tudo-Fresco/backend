from api.exceptions.validation_exception import ValidationException


class Validator:

    def __init__(self):
        self.current_field_errors = []

    def validate(self, value: str, field_name: str):
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

    def greater_than_zero(self, message: str = None):
        if self.value <= 0:
            self.current_field_errors.append(message or 'Value must be greater than 0')
        return self

    def be_posive(self, message: str = None):
        if self.value < 0:
            self.current_field_errors.append(message or 'The value must be positive')
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
