from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from api.domain.entities.user import User
from api.services.user_service import UserService
from api.shared.env_variable_manager import EnvVariableManager
from api.shared.password_hasher import PasswordHasher

class AuthService:
    def __init__(self, user_service: UserService):
        env = EnvVariableManager()
        self.user_service = user_service
        self.secret_key = env.load('JWT_SECRET_KEY', is_sensitive=True).string()
        self.algorithm = 'HS256'
        self.token_expire_minutes = env.load('USER_TOKEN_EXPIRATION_MINUTES', 60).integer()

    async def authenticate_user(self, email: str, password: str) -> str:
        service_response = await self.user_service.get_by_email(email)
        user = service_response.payload
        if not user or not PasswordHasher.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciais inválidas, verifique o seu e-mail e senha')
        return self._create_access_token({
            'sub': str(user.uuid),
            'role': user.user_access.value
        })

    async def get_user_from_token(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        service_response = await self.user_service.get(user_id)
        user = service_response.payload
        if user is None:
            raise credentials_exception
        return user

    def verify_access(self, user: User, required_access: str):
        if user.user_access.name != required_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges"
            )

    def _create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.astimezone() + (expires_delta or timedelta(minutes=self.token_expire_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
