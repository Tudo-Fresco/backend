from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.domain.entities.address import Address
from api.infrastructure.models.address_model import AddressModel
from api.infrastructure.repositories.i_repository import IRepository

class AddressRepository(IRepository[Address]):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_model(self, entity: Address) -> AddressModel:
        """Converts a domain Address entity to the SQLAlchemy AddressModel."""
        return AddressModel(
            uuid=entity.uuid,
            street=entity.street,
            city=entity.city,
            state=entity.state,
            postal_code=entity.postal_code,
            country=entity.country
        )
    
    def _from_model(self, model: AddressModel) -> Address:
        """Converts a SQLAlchemy AddressModel to a domain Address entity."""
        return Address(
            uuid=model.uuid,
            street=model.street,
            city=model.city,
            state=model.state,
            postal_code=model.postal_code,
            country=model.country
        )
    
    async def create(self, obj: Address) -> None:
        """Create a new Address in the database."""
        model = self._to_model(obj)
        self.session.add(model)
        await self.session.commit()
    
    async def get(self, obj_id: str) -> Optional[Address]:
        """Get an Address by UUID."""
        result = await self.session.execute(select(AddressModel).filter_by(uuid=obj_id))
        model = result.scalars().one_or_none()
        return self._from_model(model) if model else None
    
    async def list(self, page: int = 1, per_page: int = 10) -> List[Address]:
        """List all Addresses with pagination."""
        query = select(AddressModel).offset((page - 1) * per_page).limit(per_page)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._from_model(model) for model in models]
    
    async def update(self, obj: Address) -> None:
        """Update an Address in the database."""
        model = self._to_model(obj)
        self.session.merge(model)
        await self.session.commit()
    
    async def delete(self, obj_id: str) -> None:
        """Delete an Address by UUID."""
        result = await self.session.execute(select(AddressModel).filter_by(uuid=obj_id))
        model = result.scalars().one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
