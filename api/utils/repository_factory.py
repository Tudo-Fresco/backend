from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, TypeVar, Callable

from api.infrastructure.repositories.base_repository import BaseRepository
from api.utils.session_factory import SessionFactory

T = TypeVar('T', bound=BaseRepository)

class RepositoryFactory:

    def get_repository(
        self, 
        repo_class: Type[T], 
        session: AsyncSession
        ) -> T:
        return repo_class(session)
