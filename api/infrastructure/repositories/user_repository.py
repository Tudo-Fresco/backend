from api.domain.entities.user import User
from api.infrastructure.models.user_model import UserModel
from api.infrastructure.repositories import base_repository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(base_repository[User, UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)