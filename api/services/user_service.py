from api.controllers.models.user.user_request_model import UserRequestModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.domain.entities.user import User
from api.infrastructure.repositories.user_repository import UserRepository
from api.services.base_service import BaseService


class UserService(BaseService[UserRequestModel, UserResponseModel, User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, User)