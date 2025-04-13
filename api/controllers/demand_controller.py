from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.demand.demand_request_model import DemandRequestModel
from api.controllers.models.demand.demand_response_mode import DemandResponseModel
from api.services.i_service import IService
from api.controllers.base_controller import BaseController


class DemandController(BaseController[DemandRequestModel, DemandResponseModel]):

    def __init__(self, service: IService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=DemandRequestModel,
            response_model=DemandResponseModel,
            prefix="/demand",
            tag=__class__.__name__,
            auth_wrapper=auth_wrapper
        )