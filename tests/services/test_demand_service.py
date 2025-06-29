import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime

from api.enums.demand_status import DemandStatus
from api.enums.product_type import ProductType
from api.exceptions.unauthorized_exception import UnauthorizedException
from api.services.demand_service import DemandService


class TestDemandService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_demand_repo = AsyncMock()
        self.mock_store_repo = AsyncMock()
        self.mock_product_repo = AsyncMock()
        self.mock_user_repo = AsyncMock()
        self.mock_product_service = AsyncMock()

        self.service = DemandService(
            demand_repository=self.mock_demand_repo,
            store_repository=self.mock_store_repo,
            product_repository=self.mock_product_repo,
            user_repository=self.mock_user_repo,
            product_service=self.mock_product_service
        )

        # Mocks for input user and request (no real model instances)
        self.mock_user = MagicMock()
        self.mock_user.uuid = uuid4()
        self.mock_user.email = 'mockuser@example.com'

        self.mock_request = MagicMock()
        self.mock_request.store_uuid = uuid4()
        self.mock_request.product_uuid = uuid4()
        self.mock_request.responsible_uuid = None
        self.mock_request.needed_count = 10
        self.mock_request.description = 'Mock description'
        self.mock_request.deadline = datetime(2025, 12, 31, 23, 59, 59)
        self.mock_request.status = DemandStatus.OPENED
        self.mock_request.minimum_count = 5

        self.mock_store = MagicMock()
        self.mock_store.uuid = self.mock_request.store_uuid
        self.mock_store.owner = MagicMock()
        self.mock_store.owner.uuid = self.mock_user.uuid

        self.mock_product = MagicMock()
        self.mock_product.uuid = self.mock_request.product_uuid

        self.mock_responsible = MagicMock()
        self.mock_responsible.uuid = uuid4()

    async def test_create_calls_expected_methods_and_sets_responsible_uuid(self):
        # Arrange mocks behavior
        self.mock_store_repo.list_by_owner.return_value = [self.mock_store]
        self.mock_store_repo.get.return_value = self.mock_store
        self.mock_product_repo.get.return_value = self.mock_product
        self.mock_user_repo.get.return_value = self.mock_user
        self.mock_demand_repo.create.return_value = 'mock-demand-id'

        # Act
        response = await self.service.create(self.mock_user, self.mock_request)

        # Assert authorization check called
        self.mock_store_repo.list_by_owner.assert_awaited_once_with(self.mock_user.uuid, 1, 1_000_000)

        # Assert fetch store, product, responsible
        self.mock_store_repo.get.assert_awaited_once_with(self.mock_request.store_uuid)
        self.mock_product_repo.get.assert_awaited_once_with(self.mock_request.product_uuid)
        self.mock_user_repo.get.assert_awaited_once_with(self.mock_user.uuid)  # responsible uuid set to user.uuid

        # Assert demand created
        self.mock_demand_repo.create.assert_awaited_once()
        # Check responsible_uuid was set on the request
        self.assertEqual(self.mock_request.responsible_uuid, self.mock_user.uuid)

        # Just check response status exists (mocked ServiceResponse)
        self.assertTrue(hasattr(response, 'status'))

    async def test_create_raises_unauthorized_if_user_no_store_access(self):
        self.mock_store_repo.list_by_owner.return_value = []

        with self.assertRaises(UnauthorizedException):
            await self.service.create(self.mock_user, self.mock_request)

    async def test_get_calls_authorization_and_repo_methods(self):
        demand_id = uuid4()
        self.mock_store_repo.list_by_owner.return_value = [self.mock_store]

        mock_demand = MagicMock()
        self.mock_demand_repo.get.return_value = mock_demand
        self.mock_product_service.sign_product_images.return_value = None

        response = await self.service.get(demand_id, self.mock_user, self.mock_store.uuid)

        self.mock_store_repo.list_by_owner.assert_awaited_once_with(self.mock_user.uuid, 1, 1_000_000)
        self.mock_demand_repo.get.assert_awaited_once_with(demand_id)
        self.mock_product_service.sign_product_images.assert_awaited_once_with(mock_demand.product)
        self.assertTrue(hasattr(response, 'status'))

    async def test_get_raises_unauthorized_if_user_no_store_access(self):
        demand_id = uuid4()
        self.mock_store_repo.list_by_owner.return_value = []

        with self.assertRaises(UnauthorizedException):
            await self.service.get(demand_id, self.mock_user, self.mock_store.uuid)

    async def test_list_by_store_calls_expected_methods(self):
        self.mock_store_repo.list_by_owner.return_value = [self.mock_store]

        mock_demands = [MagicMock(), MagicMock()]
        self.mock_demand_repo.list_by_store.return_value = mock_demands
        self.mock_product_service.sign_product_images.return_value = None

        response = await self.service.list_by_store(
            self.mock_user,
            self.mock_store.uuid,
            status=DemandStatus.OPENED,
            page=1,
            per_page=10,
            radius_meters=5000,
            product_type=ProductType.ANY
        )

        self.mock_store_repo.list_by_owner.assert_awaited_once_with(self.mock_user.uuid, 1, 1_000_000)
        self.mock_demand_repo.list_by_store.assert_awaited_once_with(
            self.mock_store.uuid, DemandStatus.OPENED, 1, 10, 5000, ProductType.ANY
        )
        for demand in mock_demands:
            self.mock_product_service.sign_product_images.assert_any_await(demand.product)

        self.assertTrue(hasattr(response, 'status'))

    async def test_list_by_store_raises_unauthorized_if_no_store_access(self):
        self.mock_store_repo.list_by_owner.return_value = []

        with self.assertRaises(UnauthorizedException):
            await self.service.list_by_store(self.mock_user, self.mock_store.uuid)
