from http import HTTPStatus
from typing import Generic, TypeVar

T = TypeVar('T')

class ServiceResponse(Generic[T]):

    def __init__(self, status: HTTPStatus, message: str, payload: T = None):
        self.status: HTTPStatus = status
        self.message: str = message
        self.payload: T = payload