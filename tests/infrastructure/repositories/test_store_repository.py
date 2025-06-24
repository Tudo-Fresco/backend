import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from api.infrastructure.models.store_model import StoreModel
from api.domain.entities.store import Store
from api.infrastructure.repositories.store_repository import StoreRepository
from api.exceptions.not_found_exception import NotFoundException

class TestStoreRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = AsyncMock()
        self.repo = StoreRepository(self.session)

    def make_store_model(self) -> MagicMock:
        model = MagicMock(spec=StoreModel)
        model.to_entity.return_value = MagicMock(spec=Store)
        return model

    async def test_get_returns_store_when_found(self) -> None:
        model = self.make_store_model()
        result_mock = MagicMock()
        result_mock.scalars().one_or_none.return_value = model
        self.session.execute.return_value = result_mock
        store_id = uuid4()
        store = await self.repo.get(store_id)
        self.session.execute.assert_awaited_once()
        self.assertIsInstance(store, Store)
        model.to_entity.assert_called_once()

    async def test_get_raises_not_found_when_missing(self) -> None:
        result_mock = MagicMock()
        result_mock.scalars().one_or_none.return_value = None
        self.session.execute.return_value = result_mock
        with self.assertRaises(NotFoundException):
            await self.repo.get(uuid4())

    async def test_list_returns_stores_with_pagination(self) -> None:
        model = self.make_store_model()
        result_mock = MagicMock()
        result_mock.scalars().all.return_value = [model]
        self.session.execute.return_value = result_mock
        stores = await self.repo.list(page=2, per_page=5)
        self.session.execute.assert_awaited_once()
        self.assertIsInstance(stores, list)
        self.assertEqual(len(stores), 1)
        self.assertIsInstance(stores[0], Store)

    async def test_list_page_less_than_one_defaults_to_one(self) -> None:
        model = self.make_store_model()
        result_mock = MagicMock()
        result_mock.scalars().all.return_value = [model]
        self.session.execute.return_value = result_mock
        await self.repo.list(page=0, per_page=3)
        self.session.execute.assert_awaited_once()

    async def test_list_by_owner_returns_stores_filtered(self) -> None:
        model = self.make_store_model()
        result_mock = MagicMock()
        result_mock.scalars().all.return_value = [model]
        self.session.execute.return_value = result_mock
        owner_id = uuid4()
        stores = await self.repo.list_by_owner(owner_id, page=1, per_page=10)
        self.session.execute.assert_awaited_once()
        self.assertIsInstance(stores, list)
        self.assertEqual(len(stores), 1)
        self.assertIsInstance(stores[0], Store)

    async def test_list_by_owner_page_less_than_one_defaults_to_one(self) -> None:
        model = self.make_store_model()
        result_mock = MagicMock()
        result_mock.scalars().all.return_value = [model]
        self.session.execute.return_value = result_mock
        await self.repo.list_by_owner(uuid4(), page=0, per_page=5)
        self.session.execute.assert_awaited_once()

    async def test_get_by_cnpj_returns_store_if_found(self) -> None:
        model = self.make_store_model()
        result_mock = MagicMock()
        result_mock.scalars().first.return_value = model
        self.session.execute.return_value = result_mock
        store = await self.repo.get_by_cnpj('12345678000199')
        self.session.execute.assert_awaited_once()
        self.assertIsInstance(store, Store)
        model.to_entity.assert_called_once()

    async def test_get_by_cnpj_returns_none_if_not_found(self) -> None:
        result_mock = MagicMock()
        result_mock.scalars().first.return_value = None
        self.session.execute.return_value = result_mock
        store = await self.repo.get_by_cnpj('00000000000000')
        self.assertIsNone(store)
