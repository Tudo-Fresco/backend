from unittest.mock import MagicMock, patch
from api.domain.product import Product
from api.domain.product_name import ProductName
from api.domain.store import Store
from api.domain.certification import Certification
from api.enums.product_type import ProductType
from api.enums.unit_type import UnitType
from api.exceptions.validation_exception import ValidationException
from freezegun import freeze_time
from datetime import datetime, timezone
import unittest


class TestProduct(unittest.TestCase):

    def setUp(self) -> None:
        self.name_mock = MagicMock(spec=ProductName)
        self.store_mock = MagicMock(spec=Store)
        self.certification_mock = MagicMock(spec=Certification)
        self.product = Product(
            name=self.name_mock,
            type=ProductType.VEGETABLE,
            code="TEST001",
            unit_cost=10.0,
            unit_price=15.0,
            unit_type=UnitType.PIECE,
            unit_stock_count=100,
            image_urls=["http://example.com/image.jpg"],
            store=self.store_mock,
            certification=self.certification_mock
        )

    def test_validate_must_pass_for_all_properties(self) -> None:
        self.product.validate()
        self.name_mock.validate.assert_called_once()
        self.store_mock.validate.assert_called_once()
        self.certification_mock.validate.assert_called_once()

    def test_validate_must_not_raise_validation_exception_when_code_length_is_equal_to_limit(self) -> None:
        long_code = "a" * 1024
        product = Product(
            name=self.name_mock,
            type=ProductType.VEGETABLE,
            code=long_code,
            unit_cost=10.0,
            unit_price=15.0,
            unit_type=UnitType.PIECE,
            unit_stock_count=100,
            image_urls=["http://example.com/image.jpg"],
            store=self.store_mock
        )
        product.validate()
        self.name_mock.validate.assert_called_once()
        self.store_mock.validate.assert_called_once()

    def test_validate_must_raise_validation_exception_when_code_length_is_greater_than_limit(self) -> None:
        long_code = "a" * 1025
        product = Product(
            name=self.name_mock,
            type=ProductType.VEGETABLE,
            code=long_code,
            unit_cost=10.0,
            unit_price=15.0,
            unit_type=UnitType.PIECE,
            unit_stock_count=100,
            image_urls=["http://example.com/image.jpg"],
            store=self.store_mock
        )
        with self.assertRaises(ValidationException):
            product.validate()

    def test_validate_must_raise_validation_exception_when_unit_cost_is_negative(self) -> None:
        product = Product(
            name=self.name_mock,
            type=ProductType.VEGETABLE,
            code="TEST001",
            unit_cost=-5.0,
            unit_price=15.0,
            unit_type=UnitType.PIECE,
            unit_stock_count=100,
            image_urls=["http://example.com/image.jpg"],
            store=self.store_mock
        )
        with self.assertRaises(ValidationException):
            product.validate()

    def test_validate_must_raise_validation_exception_when_unit_price_is_zero(self) -> None:
        product = Product(
            name=self.name_mock,
            type=ProductType.VEGETABLE,
            code="TEST001",
            unit_cost=10.0,
            unit_price=0.0,
            unit_type=UnitType.PIECE,
            unit_stock_count=100,
            image_urls=["http://example.com/image.jpg"],
            store=self.store_mock
        )
        with self.assertRaises(ValidationException):
            product.validate()

    def test_validate_must_raise_validation_exception_when_unit_stock_count_is_negative(self) -> None:
        product = Product(
            name=self.name_mock,
            type=ProductType.VEGETABLE,
            code="TEST001",
            unit_cost=10.0,
            unit_price=15.0,
            unit_type=UnitType.PIECE,
            unit_stock_count=-10,
            image_urls=["http://example.com/image.jpg"],
            store=self.store_mock
        )
        with self.assertRaises(ValidationException):
            product.validate()

    def test_validate_must_call_validate_on_name_store_and_certification_if_present(self) -> None:
        product = Product(
            name=self.name_mock,
            type=ProductType.VEGETABLE,
            code="TEST001",
            unit_cost=10.0,
            unit_price=15.0,
            unit_type=UnitType.PIECE,
            unit_stock_count=100,
            image_urls=["http://example.com/image.jpg"],
            store=self.store_mock,
            certification=self.certification_mock
        )
        product.validate()
        self.name_mock.validate.assert_called_once()
        self.store_mock.validate.assert_called_once()
        self.certification_mock.validate.assert_called_once()

    def test_validate_must_not_call_validate_on_certification_if_not_present(self) -> None:
        product = Product(
            name=self.name_mock,
            type=ProductType.VEGETABLE,
            code="TEST001",
            unit_cost=10.0,
            unit_price=15.0,
            unit_type=UnitType.PIECE,
            unit_stock_count=100,
            image_urls=["http://example.com/image.jpg"],
            store=self.store_mock,
            certification=None
        )
        product.validate()
        self.name_mock.validate.assert_called_once()
        self.store_mock.validate.assert_called_once()
        self.assertEqual(0, self.certification_mock.validate.call_count)

    def test_calculate_price_must_return_correct_price(self) -> None:
        units = 5
        expected_price = 15.0 * 5
        price = self.product.calculate_price(units)
        self.assertEqual(expected_price, price)

    def test_calculate_cost_must_return_correct_cost(self) -> None:
        units = 5
        expected_cost = 10.0 * 5
        cost = self.product.calculate_cost(units)
        self.assertEqual(expected_cost, cost)

    def test_calculate_profit_must_return_correct_profit(self) -> None:
        units = 5
        expected_profit = (15.0 * 5) - (10.0 * 5)
        profit = self.product.calculate_profit(units)
        self.assertEqual(expected_profit, profit)

    def test_sell_must_decrease_stock_count_correctly(self) -> None:
        units_to_sell = -30
        expected_stock = 100 - 30
        self.product.sell(units_to_sell)
        self.assertEqual(expected_stock, self.product.unit_stock_count)

    def test_sell_must_raise_validation_exception_when_the_requested_quantity_is_not_avaiable(self) -> None:
            self.product.unit_stock_count = 0
            with self.assertRaises(ValidationException):
                self.product.sell(1)

    def test_restock_must_increase_stock_count_correctly(self) -> None:
        units_to_restock = -50
        expected_stock = 100 + 50
        self.product.restock(units_to_restock)
        self.assertEqual(expected_stock, self.product.unit_stock_count)

    @patch('api.domain.product_name.ProductName')
    @patch('api.domain.store.Store')
    def test_init_must_instance_correctly_from_a_dictionary(self, mock_store, mock_product_name) -> None:
        instance_dict = {
            "name": mock_product_name,
            "type": ProductType.VEGETABLE,
            "code": "PIM001",
            "unit_cost": 2.5,
            "unit_price": 4.0,
            "unit_type": UnitType.KILOGRAM,
            "unit_stock_count": 200,
            "image_urls": ["http://example.com/pimentao.jpg"],
            "store": mock_store,
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": "2025-03-06T12:00:00+00:00",
            "updated_at": "2025-03-06T12:00:00+00:00",
            "active": True
        }
        product = Product(**instance_dict)
        self.assertEqual(instance_dict["uuid"], str(product.uuid))
        self.assertTrue(product.active)
        self.assertEqual(instance_dict["updated_at"], product.updated_at.isoformat())
        self.assertEqual(instance_dict["created_at"], product.created_at.isoformat())
        self.assertEqual(instance_dict["name"], product.name)
        self.assertEqual(instance_dict["type"], product.type)
        self.assertEqual(instance_dict["code"], product.code)
        self.assertEqual(instance_dict["unit_cost"], product.unit_cost)
        self.assertEqual(instance_dict["unit_price"], product.unit_price)
        self.assertEqual(instance_dict["unit_type"], product.unit_type)
        self.assertEqual(instance_dict["unit_stock_count"], product.unit_stock_count)
        self.assertEqual(instance_dict["image_urls"], product.image_urls)
        self.assertEqual(instance_dict["store"], product.store)

    @freeze_time("2025-03-06 12:00:00")
    def test_activate_must_activate_correctly(self) -> None:
        product = Product(
            name=self.name_mock,
            type=ProductType.VEGETABLE,
            code="TEST001",
            unit_cost=10.0,
            unit_price=15.0,
            unit_type=UnitType.PIECE,
            unit_stock_count=100,
            image_urls=["http://example.com/image.jpg"],
            store=self.store_mock,
            active=False,
            updated_at=datetime(2025, 3, 5, 12, 0, 0, tzinfo=timezone.utc)
        )
        product.activate()
        self.assertTrue(product.active)
        self.assertEqual(
            datetime(2025, 3, 6, 12, 0, 0, tzinfo=timezone.utc),
            product.updated_at
        )

    @freeze_time("2025-03-06 12:00:00")
    def test_deactivate_must_deactivate_correctly(self) -> None:
        product = Product(
            name=self.name_mock,
            type=ProductType.VEGETABLE,
            code="TEST001",
            unit_cost=10.0,
            unit_price=15.0,
            unit_type=UnitType.PIECE,
            unit_stock_count=100,
            image_urls=["http://example.com/image.jpg"],
            store=self.store_mock,
            active=True,
            updated_at=datetime(2025, 3, 5, 12, 0, 0, tzinfo=timezone.utc)
        )
        product.deactivate()
        self.assertFalse(product.active)
        self.assertEqual(
            datetime(2025, 3, 6, 12, 0, 0, tzinfo=timezone.utc),
            product.updated_at
        )