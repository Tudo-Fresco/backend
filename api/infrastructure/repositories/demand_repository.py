from api.domain.entities.demand import Demand
from api.infrastructure.models.demand_model import DemandModel
from api.infrastructure.repositories.i_repository import IRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional


class DemandRepository(IRepository[Demand]):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_model(self, entity: Demand) -> DemandModel:
        """Converts a domain Demand entity to the SQLAlchemy DemandModel."""
        return DemandModel(
            uuid=entity.uuid,
            description=entity.description,
            quantity=entity.quantity,
            status=entity.status,
            product_uuid=entity.product_uuid,
            user_uuid=entity.user_uuid,
        )
    
    def _from_model(self, model: DemandModel) -> Demand:
        """Converts a SQLAlchemy DemandModel to a domain Demand entity."""
        return Demand(
            uuid=model.uuid,
            description=model.description,
            quantity=model.quantity,
            status=model.status,
            product_uuid=model.product_uuid,
            user_uuid=model.user_uuid,
        )
    
    async def create(self, obj: Demand) -> None:
        """Create a new Demand in the database."""
        model = self._to_model(obj)
        self.session.add(model)
        await self.session.commit()
    
    async def get(self, obj_id: str) -> Optional[Demand]:
        """Get a Demand by UUID."""
        result = await self.session.execute(select(DemandModel).filter_by(uuid=obj_id))
        model = result.scalars().one_or_none()
        return self._from_model(model) if model else None
    
    async def list(self, page: int = 1, per_page: int = 10) -> List[Demand]:
        """List all Demands with pagination."""
        query = select(DemandModel).offset((page - 1) * per_page).limit(per_page)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._from_model(model) for model in models]
    
    async def update(self, obj: Demand) -> None:
        """Update a Demand in the database."""
        model = self._to_model(obj)
        self.session.merge(model)
        await self.session.commit()
    
    async def delete(self, obj_id: str) -> None:
        """Delete a Demand by UUID."""
        result = await self.session.execute(select(DemandModel).filter_by(uuid=obj_id))
        model = result.scalars().one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
