from api.domain.entities.user import User
from api.exceptions.not_found_exception import NotFoundException
from api.infrastructure.models.user_model import UserModel
from api.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.infrastructure.repositories.repository_exception_catcher import RepositoryExceptionCatcher


class UserRepository(BaseRepository[User, UserModel]):

    catcher = RepositoryExceptionCatcher('UserRepository')


    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    @catcher
    async def get_by_email(self, email: str) -> User:
        self.logger.log_info(f'Retrieving user by email: {email}')
        result = await self.session.execute(
            select(UserModel).filter_by(email=email, active=True)
        )
        model = result.scalars().one_or_none()
        if model is None:
            self.logger.log_warning(f'Usuário não encontrado: {email}')
            raise NotFoundException(f'Active user with email {email} was not found')
        return model.to_entity()