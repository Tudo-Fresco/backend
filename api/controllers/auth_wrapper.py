from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.services.auth_service import AuthService
from api.domain.entities.user import User
from api.enums.user_access import UserAccess
from api.services.service_response import ServiceResponse
from api.shared.logger import Logger
from fastapi import Depends
from fastapi import HTTPException


class AuthWrapper:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.security = HTTPBearer()
        self.logger = Logger('AuthenticationWrapper')

    def with_access(self, required_access: list[UserAccess]):
        async def dependency(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> User:
            self.logger.log_debug('Checking access')
            token = credentials.credentials
            service_response = await self.auth_service.verify_access(token, required_access)
            user = service_response.payload
            if not user:
                raise HTTPException(
                    status_code=service_response.status,
                    detail=self.__make_response(service_response)
                )
            return user
        return dependency


    def __make_response(self, service_response: ServiceResponse) -> JSONResponse:
        return JSONResponse(
            status_code=service_response.status,
            content=jsonable_encoder({
                'payload': service_response.payload or {},
                'message': service_response.message
            })
        )