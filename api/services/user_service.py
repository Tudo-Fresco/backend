from api.clients.google_buckets_client import GoogleBucketsClient
from api.controllers.models.user.user_request_model import UserRequestModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.controllers.models.user.user_update_profile_request_model import UserUpdateProfileRequestModel
from api.domain.entities.user import User
from api.enums.bucket_name import BucketName
from api.enums.user_access import UserAccess
from api.exceptions.validation_exception import ValidationException
from api.infrastructure.repositories.user_repository import UserRepository
from api.services.base_service import BaseService
from api.services.service_exception_catcher import ServiceExceptionCatcher
from api.services.service_response import ServiceResponse
from http import HTTPStatus
from api.shared.password_hasher import PasswordHasher


class UserService(BaseService[UserRequestModel, UserResponseModel, User]):

    catch = ServiceExceptionCatcher('UserService')

    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, User, UserResponseModel)
        self.bucket_client = GoogleBucketsClient(BucketName.USER_PROFILE)

    @catch
    async def create(self, request: UserRequestModel) -> ServiceResponse[UserResponseModel]:
        self.logger.log_info('Creating a new record')
        user: User = User(**request.model_dump())
        user.validate()
        user.hash_password()
        service_response = await self.get_by_email(user.email)
        if service_response.status != HTTPStatus.NOT_FOUND:
            raise ValidationException(f'O e-mail {user.email} já está cadastrado no sistema')
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
    
    @catch
    async def upload_profile_picture(self, user_uuid: str, image_bytes: bytes, file_name: str) -> ServiceResponse[UserResponseModel]:
        self.logger.log_info(f'Uploading profile picture for user {user_uuid}')
        user: User = await self.repository.get(user_uuid)
        new_blob_name = await self.bucket_client.update_image(
            new_image_bytes=image_bytes,
            original_filename=file_name,
            old_blob_name=user.profile_picture
        )
        user.profile_picture = new_blob_name
        await self.repository.update(user)
        response = self.response_model(**user.to_dict())
        return ServiceResponse(
            status=HTTPStatus.OK,
            message='Foto de perfil atualizada com sucesso',
            payload=response
        )
    
    @catch
    async def get_profile_image_signed_url(self, user_uuid: str) -> ServiceResponse[str]:
        self.logger.log_info(f'Getting signed url profile picture for user {user_uuid}')
        user: User = await self.repository.get(user_uuid)
        signed_url: str = await self.bucket_client.read_image(user.profile_picture)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message='The URL was signed successfully',
            payload=signed_url
        )
    
    @catch
    async def update_profile(self, requester: UserResponseModel, request: UserUpdateProfileRequestModel) -> ServiceResponse[UserResponseModel]:
        self.logger.log_info(f'Updating the profile for the user: {request.email}, id: {request.uuid}')
        if str(requester.uuid) != str(request.uuid):
            self.logger.log_warning(f'The user {requester.uuid} tried to update the profile of the user {request.uuid}')
            raise ValidationException('Não é possível alterar dados de outros usuários')
        user: User = await self.repository.get(request.uuid)
        password_hasher = PasswordHasher()
        current_password_matches: bool = password_hasher.verify(request.current_password, user.password)
        if not current_password_matches:
            raise ValidationException('A senha atual está incorreta')
        user.update(**request.model_dump())
        user.validate()
        user.hash_password()
        self.logger.log_debug(f'The properties are valid and ready to be updated for the user {user.email}')
        await self.repository.update(user)
        self.logger.log_debug(f'The user {user.email} was successfully updated')
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'O usuário {user.email} foi atualizado com sucesso',
            payload=UserResponseModel(**user.to_dict())
        )