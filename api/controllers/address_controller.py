from api.controllers.models.address.address_request_model import AddressRequestModel
from api.controllers.models.address.address_response_model import AddressResponseModel
from api.services.i_service import IService
from api.controllers.base_controller import BaseController


class AddressController(BaseController[AddressRequestModel, AddressResponseModel]):

    def __init__(self, service: IService):
        super().__init__(
            service=service,
            request_model=AddressRequestModel,
            response_model=AddressResponseModel,
            prefix="/address",
            tag=__class__.__name__
        )