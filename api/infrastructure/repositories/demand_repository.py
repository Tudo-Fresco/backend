from api.domain.entities.demand import Demand
from api.infrastructure.models.demand_model import DemandModel
from api.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class DemandRepository(BaseRepository[Demand, DemandModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DemandModel)