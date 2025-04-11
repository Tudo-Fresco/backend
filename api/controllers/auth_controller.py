from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.services.auth_service import AuthService

class AuthController:
    def __init__(self, auth_service: AuthService):
        self.router = APIRouter(prefix='/auth', tags=['Auth'])
        self.auth_service = auth_service
        self.router.post('/token')(self.login)

    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
        token = await self.auth_service.authenticate_user(
            email=form_data.username,
            password=form_data.password
        )
        return {'access_token': token, 'token_type': 'bearer'}
