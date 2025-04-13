# api/controllers/auth_wrapper.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.services.auth_service import AuthService
from api.domain.entities.user import User
from api.enums.user_access import UserAccess
from api.shared.logger import Logger


class AuthWrapper:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.security = HTTPBearer()
        self.logger = Logger('AuthenticationWrapper')

    async def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> User:
        token = credentials.credentials
        user = await self.auth_service.get_user_from_token(token)
        return user

    def with_access(self, required_access: list[UserAccess]):
        async def dependency(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> User:
            self.logger.log_debug('Checking access')
            token = credentials.credentials
            user = await self.auth_service.get_user_from_token(token)
            if user.user_access not in required_access:
                raise HTTPException(status=status.HTTP_403_FORBIDDEN, detail="Access denied")
            return user
        return dependency
