from api.controllers.models.user.user_request_model import UserRequestModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.domain.entities.user import User
from api.enums.user_access import UserAccess
from api.exceptions.validation_exception import ValidationException
from api.infrastructure.repositories.user_repository import UserRepository
from api.services.base_service import BaseService
from api.services.service_exception_catcher import ServiceExceptionCatcher
from api.services.service_response import ServiceResponse
from http import HTTPStatus


class UserService(BaseService[UserRequestModel, UserResponseModel, User]):

    catch = ServiceExceptionCatcher('UserService')

    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, User, UserResponseModel)

    @catch
    async def create(self, request: UserRequestModel) -> ServiceResponse[UserResponseModel]:
        self.logger.log_info('Creating a new record')
        user: User = User(**request.model_dump())
        user.hash_password()
        await self.repository.create(user)
        response = self.response_model(**user.to_dict())
        return ServiceResponse(status=HTTPStatus.CREATED, message=f'O registro {user.uuid} foi criado com sucesso', payload=response)

    @catch
    async def get_by_email(self, email: str) -> ServiceResponse[User]:
        user: User = await self.repository.get_by_email(email)
        return ServiceResponse(status=HTTPStatus.OK, message=f'O registro {email} foi encontrado com sucesso', payload=user)
    
    @catch
    async def sign_up(self, request: UserRequestModel) -> ServiceResponse[UserResponseModel]:
        if request.user_access == UserAccess.ADMIN:
            raise ValidationException('Não é possível cadastrar-se como administrador, escolha outra opção.')
        service_response = await self.create(request)
        return service_response