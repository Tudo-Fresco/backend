from api.controllers.models.demand.demand_request_model import DemandRequestModel
from api.controllers.models.demand.demand_response_mode import DemandResponseModel
from api.domain.entities.demand import Demand
from api.infrastructure.repositories.demand_repository import DemandRepository
from api.services.base_service import BaseService


class DemandService(BaseService[DemandRequestModel, DemandResponseModel, Demand]):
    def __init__(self, demand_repository: DemandRepository):
        super().__init__(demand_repository, Demand)