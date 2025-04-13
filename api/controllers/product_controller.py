from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.models.product.product_request_model import ProductRequestModel
from api.controllers.models.product.product_response_model import ProductResponseModel
from api.services.i_service import IService
from api.controllers.base_controller import BaseController


class ProductController(BaseController[ProductRequestModel, ProductResponseModel]):

    def __init__(self, service: IService, auth_wrapper: AuthWrapper):
        super().__init__(
            service=service,
            request_model=ProductRequestModel,
            response_model=ProductResponseModel,
            prefix="/product",
            tag=__class__.__name__,
            auth_wrapper=auth_wrapper
        )