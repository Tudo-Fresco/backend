from sqlalchemy.future import select
from sqlalchemy import func
from typing import List
from api.domain.entities.product import Product
from api.enums.product_type import ProductType
from api.infrastructure.models.product_model import ProductModel
from api.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class ProductRepository(BaseRepository[Product, ProductModel]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductModel)

    async def list_by_name_and_type(
        self,
        name: str = '*',
        type: ProductType = ProductType.ANY,
        page: int = 1,
        per_page: int = 30
    ) -> List[Product]:
        self.logger.log_debug(f'Listing products by name="{name}" and type="{type.name}"')
        query = select(self.model_class).filter(self.model_class.active.is_(True))
        if name != '*':
            query = query.filter(func.unaccent(self.model_class.search_name).ilike(f'%{name}%'))
        if type != ProductType.ANY:
            query = query.filter(self.model_class.type == type)
        query = query.offset((page - 1) * per_page).limit(per_page)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [model.to_entity() for model in models]
