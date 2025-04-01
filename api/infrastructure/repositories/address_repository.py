from api.domain.entities.address import Address
from api.infrastructure.models.address_model import AddressModel
from api.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ProductRepository(BaseRepository[Address, AddressModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AddressModel)