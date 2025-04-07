from api.controllers.models.product.product_request_model import ProductRequestModel
from api.controllers.models.product.product_response_model import ProductResponseModel
from api.domain.entities.product import Product
from api.infrastructure.repositories.product_repository import ProductRepository
from api.services.base_service import BaseService


class ProductService(BaseService[ProductRequestModel, ProductResponseModel, Product]):
    def __init__(self, product_repository: ProductRepository):
        super().__init__(product_repository, Product)