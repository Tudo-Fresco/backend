from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.domain.entities.user import User
from api.infrastructure.models.user_model import UserModel
from api.infrastructure.repositories.i_repository import IRepository


class UserRepository(IRepository[User]):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_model(self, entity: User) -> UserModel:
        """Converts a domain User entity to the SQLAlchemy UserModel."""
        return UserModel(
            uuid=entity.uuid,
            username=entity.username,
            email=entity.email,
            password=entity.password,
        )
    
    def _from_model(self, model: UserModel) -> User:
        """Converts a SQLAlchemy UserModel to a domain User entity."""
        return User(
            uuid=model.uuid,
            username=model.username,
            email=model.email,
            password=model.password,
        )
    
    async def create(self, obj: User) -> None:
        """Create a new User in the database."""
        model = self._to_model(obj)
        self.session.add(model)
        await self.session.commit()
    
    async def get(self, obj_id: str) -> Optional[User]:
        """Get a User by its UUID."""
        result = await self.session.execute(select(UserModel).filter_by(uuid=obj_id))
        model = result.scalars().one_or_none()
        return self._from_model(model) if model else None
    
    async def list(self, page: int = 1, per_page: int = 10) -> List[User]:
        """List all Users with pagination."""
        query = select(UserModel).offset((page - 1) * per_page).limit(per_page)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._from_model(model) for model in models]
    
    async def update(self, obj: User) -> None:
        """Update a User in the database."""
        model = self._to_model(obj)
        self.session.merge(model)
        await self.session.commit()
    
    async def delete(self, obj_id: str) -> None:
        """Delete a User by UUID."""
        result = await self.session.execute(select(UserModel).filter_by(uuid=obj_id))
        model = result.scalars().one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
