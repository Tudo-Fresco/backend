import unittest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.entities.demand import Demand
from api.enums.demand_status import DemandStatus
from api.enums.product_type import ProductType
from api.enums.store_type import StoreType
from api.infrastructure.models.address_model import AddressModel
from api.infrastructure.models.demand_model import DemandModel
from api.infrastructure.models.store_model import StoreModel
from api.infrastructure.repositories.demand_repository import DemandRepository
from api.exceptions.not_found_exception import NotFoundException


class TestDemandRepository(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.session = AsyncMock(spec=AsyncSession)
        self.repo = DemandRepository(self.session)

    def make_valid_address(self) -> MagicMock:
        address = MagicMock(spec=AddressModel)
        address.latitude = 10.0
        address.longitude = 20.0
        return address

    def make_demand_model(self) -> MagicMock:
        model = MagicMock(spec=DemandModel)
        model.to_entity.return_value = MagicMock(spec=Demand)
        return model

    async def test_list_by_store_raises_if_store_not_found(self) -> None:
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mock_result
        with self.assertRaises(ValueError):
            await self.repo.list_by_store(uuid4())

    async def test_list_by_store_raises_if_address_invalid(self) -> None:
        store = MagicMock(spec=StoreModel)
        store.address = None
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = store
        self.session.execute.return_value = mock_result
        with self.assertRaises(ValueError):
            await self.repo.list_by_store(uuid4())

    async def test_list_by_store_for_supplier_filters_by_distance(self) -> None:
        store = MagicMock(spec=StoreModel)
        store.store_type = StoreType.SUPPLIER
        store.address = self.make_valid_address()
        demand_model = self.make_demand_model()
        store_result = MagicMock()
        store_result.scalar_one_or_none.return_value = store
        demands_result = MagicMock()
        demands_result.scalars.return_value.all.return_value = [demand_model]
        self.session.execute.side_effect = [store_result, demands_result]
        result = await self.repo.list_by_store(
            store_uuid=uuid4(),
            status=DemandStatus.ANY,
            product_type=ProductType.ANY
        )
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Demand)

    async def test_list_by_store_for_retailer_filters_by_store_uuid(self) -> None:
        store = MagicMock(spec=StoreModel)
        store.store_type = StoreType.RETAILER
        store.address = self.make_valid_address()
        demand_model = self.make_demand_model()
        store_result = MagicMock()
        store_result.scalar_one_or_none.return_value = store
        demands_result = MagicMock()
        demands_result.scalars.return_value.all.return_value = [demand_model]
        self.session.execute.side_effect = [store_result, demands_result]
        result = await self.repo.list_by_store(
            store_uuid=uuid4(),
            status=DemandStatus.OPENED,
            product_type=ProductType.ANY
        )
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Demand)

    async def test_list_by_store_applies_product_type_filter(self) -> None:
        store = MagicMock(spec=StoreModel)
        store.store_type = StoreType.RETAILER
        store.address = self.make_valid_address()
        demand_model = self.make_demand_model()
        store_result = MagicMock()
        store_result.scalar_one_or_none.return_value = store
        demands_result = MagicMock()
        demands_result.scalars.return_value.all.return_value = [demand_model]
        self.session.execute.side_effect = [store_result, demands_result]
        result = await self.repo.list_by_store(
            store_uuid=uuid4(),
            status=DemandStatus.ANY,
            product_type=ProductType.DAIRY
        )
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Demand)

    async def test_get_returns_demand_if_exists(self) -> None:
        demand_model = self.make_demand_model()
        result_mock = MagicMock()
        result_mock.scalars.return_value.one_or_none.return_value = demand_model
        self.session.execute.return_value = result_mock
        result = await self.repo.get(uuid4())
        self.assertIsInstance(result, Demand)

    async def test_get_raises_if_not_found(self) -> None:
        result_mock = MagicMock()
        result_mock.scalars.return_value.one_or_none.return_value = None
        self.session.execute.return_value = result_mock
        with self.assertRaises(NotFoundException):
            await self.repo.get(uuid4())
