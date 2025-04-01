from api.domain.entities.demand import Demand
from api.infrastructure.models.demand_model import DemandModel
from api.infrastructure.repositories import base_repository
from sqlalchemy.ext.asyncio import AsyncSession


class ProductRepository(base_repository[Demand, DemandModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DemandModel)