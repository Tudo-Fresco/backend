from typing import List
from uuid import UUID
from sqlalchemy import func, literal
from api.domain.entities.demand import Demand
from api.enums.demand_status import DemandStatus
from api.enums.product_type import ProductType
from api.enums.store_type import StoreType
from api.exceptions.not_found_exception import NotFoundException
from api.infrastructure.models.address_model import AddressModel
from api.infrastructure.models.demand_model import DemandModel
from api.infrastructure.repositories.repository_exception_catcher import RepositoryExceptionCatcher
from api.infrastructure.models.product_model import ProductModel
from api.infrastructure.models.store_model import StoreModel
from api.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select


class DemandRepository(BaseRepository[Demand, DemandModel]):

    catcher = RepositoryExceptionCatcher('DemandRepository')

    def __init__(self, session: AsyncSession):
        super().__init__(session, DemandModel)

    @catcher
    async def list_by_store(self, store_uuid: UUID, status: DemandStatus = DemandStatus.ANY,
                            page: int = 1, per_page: int = 10,
                            radius_meters: int = 10000,
                            product_type: ProductType = ProductType.ANY) -> List[Demand]:
        """
        Retrieve a paginated list of demands based on a store UUID with optional filters.

        Args:
            store_uuid (UUID): The UUID of the store to filter demands by.
            status (DemandStatus): Filter by demand status (default: ANY).
            page (int): Page number for pagination (default: 1).
            per_page (int): Number of items per page (default: 10).
            radius_meters (int): Radius in meters for supplier stores (default: 10000).
            product_type (ProductType): Filter by product type (default: ANY).

        Returns:
            List[Demand]: A list of Demand entities matching the criteria.

        Raises:
            ValueError: If the store or its address is not found.
        """
        self.logger.log_debug(f'Listing demands by store: {store_uuid}, status: {status.value}, page: {page}, per_page: {per_page}')
        if page < 1:
            page = 1
        store_query = select(StoreModel).options(joinedload(StoreModel.address)).filter_by(uuid=store_uuid)
        store_result = await self.session.execute(store_query)
        store_model: StoreModel = store_result.scalar_one_or_none()
        if not store_model:
            raise ValueError(f"Store with UUID {store_uuid} not found")
        if not store_model.address or store_model.address.latitude is None or store_model.address.longitude is None:
            raise ValueError(f"Store address for UUID {store_uuid} is invalid")

        is_supplier = store_model.store_type == StoreType.SUPPLIER
        
        if is_supplier:
            supplier_lat = store_model.address.latitude
            supplier_lon = store_model.address.longitude
            demand_lat = AddressModel.latitude
            demand_lon = AddressModel.longitude
            
            delta_lat = demand_lat - literal(supplier_lat)
            delta_lon = demand_lon - literal(supplier_lon)
            
            a = (
                func.pow(func.sin(func.radians(delta_lat) / 2), 2) +
                func.cos(func.radians(literal(supplier_lat))) * func.cos(func.radians(demand_lat)) * 
                func.pow(func.sin(func.radians(delta_lon) / 2), 2)
            )
            c = 2 * func.atan2(func.sqrt(a), func.sqrt(1 - a))
            distance = literal(6371000) * c
            
            query = (
                select(DemandModel)
                .join(StoreModel, DemandModel.store_uuid == StoreModel.uuid)
                .join(AddressModel, StoreModel.address_uuid == AddressModel.uuid)
                .filter(DemandModel.active == True)
                .filter(AddressModel.latitude.isnot(None), AddressModel.longitude.isnot(None))
                .filter(distance <= radius_meters)
            )
        else:
            query = select(DemandModel).filter(
                DemandModel.store_uuid == store_uuid,
                DemandModel.active == True
            )
        
        if status != DemandStatus.ANY:
            query = query.filter(DemandModel.status == status)
        if product_type != ProductType.ANY:
            query = query.join(ProductModel, DemandModel.product_uuid == ProductModel.uuid).filter(
                ProductModel.type == product_type
            )
        
        query = query.options(
            joinedload(DemandModel.store).joinedload(StoreModel.address),
            joinedload(DemandModel.product),
            joinedload(DemandModel.responsible)
        ).offset((page - 1) * per_page).limit(per_page)
        
        result = await self.session.execute(query)
        models = result.scalars().all()
        self.logger.log_debug(f"Found {len(models)} demands")
        demands = [model.to_entity() for model in models]
        return demands
    
    async def get(self, obj_id: UUID) -> Demand:
        self.logger.log_debug(f'Retrieving the demand: {obj_id}')
        query = (
            select(self.model_class)
            .filter_by(uuid=obj_id, active=True)
            .options(
                joinedload(DemandModel.responsible),
                joinedload(DemandModel.product),
                joinedload(DemandModel.store).joinedload(StoreModel.address),
                joinedload(DemandModel.store).joinedload(StoreModel.owner)
            )
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            self.logger.log_warning(f'No active demand found for UUID: {obj_id}')
            raise NotFoundException(f'Nenhuma demanda com o id {obj_id} foi encontrada')
        return model.to_entity()