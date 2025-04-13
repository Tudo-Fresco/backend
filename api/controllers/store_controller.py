from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.store.store_request_model import StoreRequestModel
from api.controllers.models.store.store_response_model import StoreResponseModel
from api.services.i_service import IService
from api.controllers.base_controller import BaseController


class StoreController(BaseController[StoreRequestModel, StoreResponseModel]):

    def __init__(self, service: IService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=StoreRequestModel,
            response_model=StoreResponseModel,
            prefix="/store",
            tag=__class__.__name__,
            auth_wrapper=auth_wrapper
        )