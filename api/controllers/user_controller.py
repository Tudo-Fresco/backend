from fastapi.responses import JSONResponse
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.user.user_request_model import UserRequestModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.controllers.models.user.user_update_profile_request_model import UserUpdateProfileRequestModel
from api.enums.user_access import UserAccess
from api.services.i_service import IService
from api.controllers.base_controller import BaseController
from fastapi import Body, Depends, File, UploadFile
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
        self.router.add_api_route(
            path='/profile-picture',
            endpoint=self._upload_profile_picture_handler(),
            methods=['POST'],
            response_model=UserResponseModel,
            status_code=200,
            summary=f'Upload Profile Picture for {self.__class__.__name__}'
        )
        self.router.add_api_route(
            path='/signed-profile-picture',
            endpoint=self._get_signed_profile_image_url_handler(),
            methods=['GET'],
            response_model=UserResponseModel,
            status_code=200,
            summary='Returns a signed URL to display the profile picture'
        )
        self.router.add_api_route(
            path='/profile',
            endpoint=self._update_profile_handler(),
            methods=['PUT'],
            response_model=UserResponseModel,
            status_code=200,
            summary='Updates the user profile'
        )

    def _sign_up_handler(self):
        async def sign_up(model: UserRequestModel = Body(...)) -> JSONResponse:
            self.logger.log_info(f'Creating a new user, e-mail: {model.email}')
            service_response: ServiceResponse = await self.service.sign_up(request=model)
            return self.make_response(service_response)
        return sign_up
    

    def _upload_profile_picture_handler(self):
            async def upload_profile_picture(
                file: UploadFile = File(...),
                user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.ANY]))
            ) -> JSONResponse:
                self.logger.log_info(f'Handling profile picture upload for user {user.uuid}')
                image_bytes = await file.read()
                file_name = file.filename
                service_response: ServiceResponse = await self.service.upload_profile_picture(
                    user_uuid=user.uuid,
                    image_bytes=image_bytes,
                    file_name=file_name
                )
                return self.make_response(service_response)
            return upload_profile_picture
    
    def _get_signed_profile_image_url_handler(self):
        async def get_signed_profile_image_url(user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.ANY]))) -> JSONResponse:
            self.logger.log_info(f'Signing the profile image url for the user {user.uuid}')
            service_response: ServiceResponse = await self.service.get_profile_image_signed_url(user.uuid)
            return self.make_response(service_response)
        return get_signed_profile_image_url
    
    def _update_profile_handler(self):
         async def update_profile(request: UserUpdateProfileRequestModel = Body(...),
                                  user: UserResponseModel = Depends(self.auth_wrapper.with_access([UserAccess.ANY]))) -> JSONResponse:
            self.logger.log_info(f'Updating the profile of the user {request.uuid}')
            service_response: ServiceResponse = await self.service.update_profile(user, request)
            return self.make_response(service_response)
         return update_profile