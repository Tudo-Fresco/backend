import unittest
from unittest.mock import MagicMock
from api.infrastructure.models.product_model import ProductModel
from api.domain.entities.product import Product
from api.enums.unit_type import UnitType
from api.enums.product_type import ProductType


class TestProductModel(unittest.TestCase):

    def setUp(self) -> None:
        self.product_entity = Product(
            name="Test Product",
            unit_type=UnitType.KILOGRAM,
            type=ProductType.DAIRY,
            images=["img1.png", "img2.png"],
            search_name="Test Product (kg)"
        )

    def test_from_entity_populates_model_fields(self) -> None:
        model = ProductModel()
        model._from_entity(self.product_entity)
        self.assertEqual(model.name, self.product_entity.name)
        self.assertEqual(model.unit_type, self.product_entity.unit_type)
        self.assertEqual(model.type, self.product_entity.type)
        self.assertEqual(model.images, self.product_entity.images)
        self.assertEqual(model.search_name, self.product_entity.search_name)

    def test_to_entity_returns_product_with_correct_fields(self) -> None:
        model = ProductModel()
        model.name = "Another Product"
        model.unit_type = UnitType.GRAM
        model.type = ProductType.BEEF
        model.images = ["imgA.png"]
        model.search_name = "Another Product (g)"
        product_entity = model._to_entity()
        self.assertEqual(product_entity.name, model.name)
        self.assertEqual(product_entity.unit_type, model.unit_type)
        self.assertEqual(product_entity.type, model.type)
        self.assertEqual(product_entity.images, model.images)
        self.assertEqual(product_entity.search_name, model.search_name)