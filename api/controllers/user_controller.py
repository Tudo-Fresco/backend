from fastapi.responses import JSONResponse
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.user.user_request_model import UserRequestModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.services.i_service import IService
from api.controllers.base_controller import BaseController
from fastapi import APIRouter, Body, Depends, Query

from api.services.service_response import ServiceResponse


class UserController(BaseController[UserRequestModel, UserResponseModel]):

    def __init__(self, service: IService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=UserRequestModel,
            response_model=UserResponseModel,
            prefix='/user',
            tag=self.__class__.__name__,
            auth_wrapper=auth_wrapper
        )
        self.router.add_api_route(
            path='/sign-up',
            endpoint=self._sign_up_handler(),
            methods=['POST'],
            response_model=UserResponseModel,
            status_code=201,
            summary=f'Sign Up {self.__class__.__name__}',
        )

    def _sign_up_handler(self):
        async def sign_up(model: UserRequestModel = Body(...)) -> JSONResponse:
            self.logger.log_info(f'Creating a new user, e-mail: {model.email}')
            service_response: ServiceResponse = await self.service.sign_up(request=model)
            return self.make_response(service_response)
        return sign_up