from api.exceptions.custom_exception import CustomException
from http import HTTPStatus


class ValidationException(CustomException):
    def __init__(self, message: str, status: HTTPStatus = HTTPStatus.BAD_REQUEST) -> None:
        super().__init__(message, status)