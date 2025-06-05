from http import HTTPStatus
from api.services.service_response import ServiceResponse
from api.controllers.models.product.product_request_model import ProductRequestModel
from api.controllers.models.product.product_response_model import ProductResponseModel
from api.infrastructure.repositories.product_repository import ProductRepository
from api.domain.entities.product import Product
from api.enums.product_type import ProductType
from api.services.base_service import BaseService
from typing import List



class ProductService(BaseService[ProductRequestModel, ProductResponseModel, Product]):
    def __init__(self, product_repository: ProductRepository):
        super().__init__(product_repository, Product, ProductResponseModel)
    
    async def list_by_name_and_type(self, name: str = '*', type: ProductType = ProductType.ANY, page: int = 1, per_page: int = 30) -> ServiceResponse[List[Product]]:
        products = await self.repository.list_by_name_and_type(name, type, page, per_page)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'{len(products)} produtos foram encontrados relacionados relacionados com o nome: {name} e tipo {type.value}',
            payload=self._convert_many_to_response(products)
        )