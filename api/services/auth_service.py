from datetime import datetime, timedelta
from jose import ExpiredSignatureError, JWTError, jwt
from fastapi import HTTPException, status
from api.domain.entities.user import User
from api.enums.user_access import UserAccess
from api.services.user_service import UserService
from api.shared.env_variable_manager import EnvVariableManager
from api.shared.logger import Logger
from api.shared.password_hasher import PasswordHasher


class AuthService:
    def __init__(self, user_service: UserService):
        env = EnvVariableManager()
        self.user_service = user_service
        self.secret_key = env.load('JWT_SECRET_KEY', is_sensitive=True).string()
        self.algorithm = 'HS256'
        self.token_expire_minutes = env.load('USER_TOKEN_EXPIRATION_MINUTES', 60).integer()
        self.sessions_cache: dict[str, User] = {}
        self.logger = Logger('AuthService')

    async def authenticate_user(self, email: str, password: str) -> str:
        self.logger.log_debug(f'Providing a new JWT token for the user {email}')
        service_response = await self.user_service.get_by_email(email)
        user = service_response.payload
        valid_password: bool = PasswordHasher.verify(password, user.password)
        if not user or not valid_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciais inválidas, verifique o seu e-mail e senha')
        jwt_body: dict = {
            'sub': str(user.uuid),
            'role': user.user_access.value
        }
        expires = timedelta(minutes=self.token_expire_minutes)
        access_token = self._create_access_token(jwt_body, expires)
        return access_token

    async def verify_access(self, token: str, required_access: list[UserAccess]) -> User | None:
        user: User = await self._get_user_from_token(token)
        if user.user_access not in required_access:
            self.logger.log_info('The user is not authorized')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Usuário não autorizado'
            )
        self.logger.log_debug('The user is authorized')
        return user
        
    async def _get_user_from_token(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválidas',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get('sub')
            if user_id is None:
                raise credentials_exception
        except ExpiredSignatureError as ex:
            self.logger.log_warning('This user session is expeired')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Sua sessão expirou, fazer o login novamente',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        except JWTError as ex:
            self.logger.log_error(str(ex))
            raise credentials_exception
        self.logger.log_debug(f'Getting user {user_id}')
        service_response = await self.user_service.get(user_id)
        user = service_response.payload
        if user is None:
            raise credentials_exception
        return user

    def _create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now().astimezone() + (expires_delta or timedelta(minutes=self.token_expire_minutes))
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)