from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.user.user_request_model import UserRequestModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.services.i_service import IService
from api.controllers.base_controller import BaseController


class UserController(BaseController[UserRequestModel, UserResponseModel]):

    def __init__(self, service: IService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=UserRequestModel,
            response_model=UserResponseModel,
            prefix="/user",
            tag=self.__class__.__name__,
            auth_wrapper=auth_wrapper
        )