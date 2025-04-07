from api.domain.entities.product import Product
from api.infrastructure.models.product_model import ProductModel
from api.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ProductRepository(BaseRepository[Product, ProductModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductModel)