from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.domain.entities.product import Product
from api.infrastructure.models.product_model import ProductModel
from api.infrastructure.repositories.i_repository import IRepository


class ProductRepository(IRepository[Product]):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_model(self, entity: Product) -> ProductModel:
        """Converts a domain Product entity to the SQLAlchemy ProductModel."""
        return ProductModel(
            uuid=entity.uuid,
            name=entity.name,
            description=entity.description,
            price=entity.price,
            stock_quantity=entity.stock_quantity
        )
    
    def _from_model(self, model: ProductModel) -> Product:
        """Converts a SQLAlchemy ProductModel to a domain Product entity."""
        return Product(
            uuid=model.uuid,
            name=model.name,
            description=model.description,
            price=model.price,
            stock_quantity=model.stock_quantity
        )
    
    async def create(self, obj: Product) -> None:
        """Create a new Product in the database."""
        model = self._to_model(obj)
        self.session.add(model)
        await self.session.commit()
    
    async def get(self, obj_id: str) -> Optional[Product]:
        """Get a Product by UUID."""
        result = await self.session.execute(select(ProductModel).filter_by(uuid=obj_id))
        model = result.scalars().one_or_none()
        return self._from_model(model) if model else None
    
    async def list(self, page: int = 1, per_page: int = 10) -> List[Product]:
        """List all Products with pagination."""
        query = select(ProductModel).offset((page - 1) * per_page).limit(per_page)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._from_model(model) for model in models]
    
    async def update(self, obj: Product) -> None:
        """Update a Product in the database."""
        model = self._to_model(obj)
        self.session.merge(model)
        await self.session.commit()
    
    async def delete(self, obj_id: str) -> None:
        """Delete a Product by UUID."""
        result = await self.session.execute(select(ProductModel).filter_by(uuid=obj_id))
        model = result.scalars().one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
