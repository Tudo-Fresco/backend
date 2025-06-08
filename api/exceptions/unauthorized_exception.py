from api.exceptions.custom_exception import CustomException
from http import HTTPStatus


class UnauthorizedException(CustomException):

    def __init__(self, message) -> None:
        super().__init__(message, HTTPStatus.UNAUTHORIZED)