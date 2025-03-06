from http import HTTPStatus


class ValidationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message: str = message
        self.status_code: HTTPStatus = HTTPStatus.BAD_REQUEST