# api/controllers/auth_wrapper.py
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.services.auth_service import AuthService
from api.domain.entities.user import User
from api.enums.user_access import UserAccess
from api.shared.logger import Logger
from fastapi import Depends
from fastapi import HTTPException, status


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
                raise HTTPException(status_code=service_response.status, detail=service_response.message)
            return user
        return dependency
