from http import HTTPStatus
from api.controllers.models.user.user_request_model import UserRequestModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.domain.entities.user import User
from api.infrastructure.repositories.user_repository import UserRepository
from api.services.base_service import BaseService
from api.services.service_response import ServiceResponse


class UserService(BaseService[UserRequestModel, UserResponseModel, User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, User, UserResponseModel)

    async def get_by_email(self, email: str) -> ServiceResponse[User]:
        user: User = await self.repository.get_by_email(email)
        return ServiceResponse(status=HTTPStatus.OK, message=f'O registro {email} foi encontrado com sucesso', payload=user)