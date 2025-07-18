from api.exceptions.custom_exception import CustomException
from api.services.service_response import ServiceResponse
from api.shared.logger import Logger
from http import HTTPStatus
import traceback
from starlette.exceptions import HTTPException as StarletteHTTPException


class ServiceExceptionCatcher:

    def __init__(self, service_name: str) -> None:
        self.service_name = service_name
        self.logger = Logger(self.service_name)

    def __call__(self, func):
        async def inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as exception:
                self.logger.log_error(f'An error occurred: {exception}')
                self.logger.log_debug(f'Exception details: {traceback.format_exc()}')
                response = ServiceResponse(
                    status=self.get_status(exception),
                    message=self.get_message(exception)
                )
                return response
        return inner

    def get_status(self, exception: Exception) -> HTTPStatus:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if isinstance(exception, CustomException):
            status = exception.status
        if isinstance(exception, StarletteHTTPException):
            status = exception.status_code
        return status
    
    def get_message(self, exception: Exception) -> str:
        message: str = 'Algo inesperado aconteceu, contatar suporte.'
        if isinstance(exception, CustomException):
            message = exception.message
        if isinstance(exception, StarletteHTTPException):
            message = exception.detail
        self.logger.log_warning(message)
        self.logger.log_error(str(exception))
        return message
