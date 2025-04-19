from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from api.services.auth_service import AuthService
from api.services.service_response import ServiceResponse
from fastapi.encoders import jsonable_encoder


class AuthController:

    def __init__(self, auth_service: AuthService):
        self.router = APIRouter(prefix='/auth', tags=['Auth'])
        self.auth_service = auth_service
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
        self._add_routes()

    def _add_routes(self):
        @self.router.post('/login')
        async def login(form_data: OAuth2PasswordRequestForm = Depends()):
            service_response: ServiceResponse = await self.auth_service.authenticate_user(
                email=form_data.username,
                password=form_data.password
            )
            return self.make_content(service_response)
        
    def make_content(self, service_response: ServiceResponse) -> dict[str, Any]:
        payload = service_response.payload
        return jsonable_encoder({
            'payload': payload or {},
            'message': service_response.message
        })