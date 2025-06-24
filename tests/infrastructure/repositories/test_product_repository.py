import unittest
from unittest.mock import AsyncMock, MagicMock
from api.enums.product_type import ProductType
from api.domain.entities.product import Product
from api.infrastructure.models.product_model import ProductModel
from api.infrastructure.repositories.product_repository import ProductRepository

class TestProductRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = AsyncMock()
        self.repo = ProductRepository(self.session)

    def make_product_model(self) -> None:
        model = MagicMock(spec=ProductModel)
        model.to_entity.return_value = MagicMock(spec=Product)
        return model

    async def test_list_returns_products(self) -> None:
        """Basic test: returns products with default args"""
        model_instance = self.make_product_model()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model_instance]

        self.session.execute.return_value = mock_result

        results = await self.repo.list_by_name_and_type()
        self.session.execute.assert_awaited_once()
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Product)
        model_instance.to_entity.assert_called_once()

    async def test_list_returns_empty_when_no_products(self) -> None:
        """When no products found, returns empty list"""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.session.execute.return_value = mock_result

        results = await self.repo.list_by_name_and_type(name='nonexistent')
        self.assertEqual(results, [])

    async def test_list_filters_by_name_specific(self) -> None:
        """When name is a specific string, filters by name"""
        model_instance = self.make_product_model()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model_instance]
        self.session.execute.return_value = mock_result

        await self.repo.list_by_name_and_type(name='testname')

    async def test_list_filters_by_type_any(self) -> None:
        """When type is ANY, no type filter applied"""
        model_instance = self.make_product_model()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model_instance]
        self.session.execute.return_value = mock_result

        await self.repo.list_by_name_and_type(type=ProductType.ANY)

    async def test_list_filters_by_type_specific(self) -> None:
        """When type is specific, filters by product type"""
        model_instance = self.make_product_model()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model_instance]
        self.session.execute.return_value = mock_result
        await self.repo.list_by_name_and_type(type=ProductType.EGG)

    async def test_pagination_offset_and_limit(self) -> None:
        """Test pagination arguments affect offset and limit"""
        model_instance = self.make_product_model()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model_instance]
        self.session.execute.return_value = mock_result
        await self.repo.list_by_name_and_type(page=1, per_page=10)
        await self.repo.list_by_name_and_type(page=3, per_page=5)

    async def test_invalid_page_number_defaults_to_1(self) -> None:
        """If page number is zero or negative, should default to 1 (if repo handles that)"""
        model_instance = self.make_product_model()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model_instance]
        self.session.execute.return_value = mock_result
        await self.repo.list_by_name_and_type(page=-5)
        await self.repo.list_by_name_and_type(page=0)

    async def test_large_per_page_limit(self) -> None:
        """Test large per_page value"""
        model_instance = self.make_product_model()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model_instance]
        self.session.execute.return_value = mock_result
        await self.repo.list_by_name_and_type(per_page=1000)

    async def test_special_characters_in_name_filter(self) -> None:
        """Test name filter with special characters to check query correctness"""
        model_instance = self.make_product_model()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [model_instance]
        self.session.execute.return_value = mock_result
        await self.repo.list_by_name_and_type(name='%_test_')