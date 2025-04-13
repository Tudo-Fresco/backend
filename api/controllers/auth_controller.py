from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from api.services.auth_service import AuthService


class AuthController:
    def __init__(self, auth_service: AuthService):
        self.router = APIRouter(prefix='/auth', tags=['Auth'])
        self.auth_service = auth_service
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
        self._add_routes()

    def _add_routes(self):
        @self.router.post('/login')
        async def login(form_data: OAuth2PasswordRequestForm = Depends()):
            token = await self.auth_service.authenticate_user(
                email=form_data.username,
                password=form_data.password
            )
            return {'access_token': token, 'token_type': 'bearer'}