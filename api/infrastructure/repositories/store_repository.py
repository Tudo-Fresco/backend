from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.domain.entities.store import Store
from api.infrastructure.models.store_model import StoreModel
from api.infrastructure.repositories.i_repository import IRepository


class StoreRepository(IRepository[Store]):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_model(self, entity: Store) -> StoreModel:
        """Converts a domain Store entity to the SQLAlchemy StoreModel."""
        return StoreModel(
            uuid=entity.uuid,
            trade_name=entity.trade_name,
            legal_name=entity.legal_name,
            reputation=entity.reputation,
            cnpj=entity.cnpj,
            owner_uuid=entity.owner_uuid,
            legal_phone_contact=entity.legal_phone_contact,
            preferred_phone_contact=entity.preferred_phone_contact,
            legal_email_contact=entity.legal_email_contact,
            preferred_email_contact=entity.preferred_email_contact,
        )
    
    def _from_model(self, model: StoreModel) -> Store:
        """Converts a SQLAlchemy StoreModel to a domain Store entity."""
        return Store(
            uuid=model.uuid,
            trade_name=model.trade_name,
            legal_name=model.legal_name,
            reputation=model.reputation,
            cnpj=model.cnpj,
            owner_uuid=model.owner_uuid,
            legal_phone_contact=model.legal_phone_contact,
            preferred_phone_contact=model.preferred_phone_contact,
            legal_email_contact=model.legal_email_contact,
            preferred_email_contact=model.preferred_email_contact,
        )
    
    async def create(self, obj: Store) -> None:
        """Create a new Store in the database."""
        model = self._to_model(obj)
        self.session.add(model)
        await self.session.commit()
    
    async def get(self, obj_id: str) -> Optional[Store]:
        """Get a Store by UUID."""
        result = await self.session.execute(select(StoreModel).filter_by(uuid=obj_id))
        model = result.scalars().one_or_none()
        return self._from_model(model) if model else None
    
    async def list(self, page: int = 1, per_page: int = 10) -> List[Store]:
        """List all Stores with pagination."""
        query = select(StoreModel).offset((page - 1) * per_page).limit(per_page)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._from_model(model) for model in models]
    
    async def update(self, obj: Store) -> None:
        """Update a Store in the database."""
        model = self._to_model(obj)
        self.session.merge(model)
        await self.session.commit()
    
    async def delete(self, obj_id: str) -> None:
        """Delete a Store by UUID."""
        result = await self.session.execute(select(StoreModel).filter_by(uuid=obj_id))
        model = result.scalars().one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
