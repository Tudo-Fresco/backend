from http import HTTPStatus


class NotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message: str = message
        self.status_code: HTTPStatus = HTTPStatus.NOT_FOUND