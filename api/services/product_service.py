from http import HTTPStatus
from uuid import UUID
from api.clients.google_buckets_client import GoogleBucketsClient
from api.enums.bucket_name import BucketName
from api.services.service_exception_catcher import ServiceExceptionCatcher
from api.services.service_response import ServiceResponse
from api.controllers.models.product.product_request_model import ProductRequestModel
from api.controllers.models.product.product_response_model import ProductResponseModel
from api.infrastructure.repositories.product_repository import ProductRepository
from api.domain.entities.product import Product
from api.enums.product_type import ProductType
from api.services.base_service import BaseService
from typing import List



class ProductService(BaseService[ProductRequestModel, ProductResponseModel, Product]):

    catch = ServiceExceptionCatcher('ProductService')

    def __init__(self, product_repository: ProductRepository):
        super().__init__(product_repository, Product, ProductResponseModel)
        self.bucket_client = GoogleBucketsClient(BucketName.PRODUCT_IMAGES)
    
    async def list_by_name_and_type(self, name: str = '*', type: ProductType = ProductType.ANY, page: int = 1, per_page: int = 30) -> ServiceResponse[List[Product]]:
        products = await self.repository.list_by_name_and_type(name, type, page, per_page)
        await self.__sign_products_images(products)
        return ServiceResponse(
            status=HTTPStatus.OK,
            message=f'{len(products)} produtos foram encontrados relacionados relacionados com o nome: {name} e tipo {type.value}',
            payload=self._convert_many_to_response(products)
        )
    
    @catch
    async def upload_picture(self, product_uuid: UUID, image_bytes: bytes, file_name: str) -> ServiceResponse[ProductResponseModel]:
        self.logger.log_info(f'Uploading a new image for the product {product_uuid}')
        product: Product = await self.repository.get(product_uuid)
        new_blob_name = await self.bucket_client.save_image(
            new_image_bytes=image_bytes,
            original_filename=file_name
        )
        product.add_image(new_blob_name)
        await self.repository.update(product)
        response = self.response_model(**product.to_dict())
        return ServiceResponse(
            status=HTTPStatus.OK,
            message='A foto deste produto foi adicionada com sucesso',
            payload=response
        )
    
    @catch
    async def delete_picture(self, product_uuid: UUID, image_index: str) -> ServiceResponse[ProductResponseModel]:
        self.logger.log_info(f'Deleting the image {image_index} for the product {product_uuid}')
        product: Product = await self.repository.get(product_uuid)
        blob_name = product.get_image(image_index)
        await self.bucket_client.delete_image(blob_name=blob_name)
        product.delete_image(blob_name)
        await self.repository.update(product)
        response = self.response_model(**product.to_dict())
        return ServiceResponse(
            status=HTTPStatus.OK,
            message='A foto deste produto foi removida com sucesso',
            payload=response
        )

    @catch
    async def get(self, obj_id: UUID) -> ServiceResponse[ProductResponseModel]:
        self.logger.log_info(f'Reading from id {obj_id}')
        product: Product = await self.repository.get(obj_id)
        await self.__sign_product_images(product)
        self._raise_not_found_when_none(product, obj_id)
        response = self.response_model(**product.to_dict())
        return ServiceResponse(status=HTTPStatus.OK, message=f'O produto {obj_id} foi encontrado com sucesso', payload=response)

    @catch
    async def list(self, page: int = 1, per_page: int = 10) -> ServiceResponse[List[ProductResponseModel]]:
        self.logger.log_info(f'Reading many products. Page: {page}, per page: {per_page}')
        products = await self.repository.list(page, per_page)
        await self.__sign_products_images(products)
        products_response = self._convert_many_to_response(products)
        return ServiceResponse(status=HTTPStatus.OK, message=f'Leu {len(products_response)} produtos com sucesso', payload=products_response)

    async def __sign_products_images(self, products: List[Product]) -> None:
        for product in products:
            await self.__sign_product_images(product)

    async def __sign_product_images(self, product: Product) -> None:
        images: List[str] = product.images
        signed_image_urls: List[str] = []
        for img in images:
            signed_image: str = await self.bucket_client.read_image(img)
            signed_image_urls.append(signed_image)
        product.images = signed_image_urls

    
