import unittest
from unittest.mock import patch
from api.domain.entities.product import Product
from api.enums.product_type import ProductType
from api.enums.unit_type import UnitType


class TestProduct(unittest.TestCase):

    def setUp(self) -> None:
        self.product = Product(
            name="Test Product",
            unit_type=UnitType.KILOGRAM,
            type=ProductType.GRAIN,
            images=["image1.jpg", "image2.jpg"],
            search_name=""
        )

    def test_initialization_sets_properties(self) -> None:
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.unit_type, UnitType.KILOGRAM)
        self.assertEqual(self.product.type, ProductType.GRAIN)
        self.assertListEqual(self.product.images, ["image1.jpg", "image2.jpg"])
        self.assertTrue(self.product.search_name.startswith("Test Product"))

    def test_initialization_keeps_provided_search_name(self) -> None:
        p = Product(
            name="Another",
            unit_type=UnitType.GRAM,
            type=ProductType.SPICE,
            images=[],
            search_name="custom search"
        )
        self.assertEqual(p.search_name, "custom search")

    @patch("api.domain.entities.product.Validator")
    def test_validate_calls_validator_methods(self, mock_validator) -> None:
        mock_validator = mock_validator.return_value
        self.product.validate()
        mock_validator.on.assert_called_once_with(self.product.name, "Nome do produto")
        mock_validator.on().character_limit.assert_called_once_with(256, "Deve ser menor do que 256 caracteres.")
        mock_validator.on().character_limit().not_empty.assert_called_once_with("É obrigatório")
        mock_validator.check.assert_called_once()

    def test_add_image_appends_to_images(self) -> None:
        new_image = "image3.jpg"
        self.product.add_image(new_image)
        self.assertIn(new_image, self.product.images)

    def test_delete_image_removes_existing_image(self) -> None:
        image_to_remove = "image1.jpg"
        self.product.delete_image(image_to_remove)
        self.assertNotIn(image_to_remove, self.product.images)

    def test_delete_image_ignores_nonexistent_image(self) -> None:
        before = list(self.product.images)
        self.product.delete_image("not_in_list.jpg")
        self.assertListEqual(before, self.product.images)

    def test_get_image_returns_correct_image(self) -> None:
        self.assertEqual(self.product.get_image(1), "image2.jpg")

    def test_get_image_returns_none_for_invalid_index(self) -> None:
        self.assertIsNone(self.product.get_image(-1))
        self.assertIsNone(self.product.get_image(100))

    def test_get_search_name_format(self) -> None:
        expected = "Test Product (kg)"
        actual = self.product._get_search_name()
        self.assertEqual(actual, expected)

    def test_get_type_abbreviation_known_types(self) -> None:
        self.assertEqual(self.product._get_type_abbreviation(UnitType.KILOGRAM), "kg")
        self.assertEqual(self.product._get_type_abbreviation(UnitType.PIECE), "uni.")
        self.assertEqual(self.product._get_type_abbreviation(UnitType.METRIC_TON), "t")
        self.assertEqual(self.product._get_type_abbreviation(UnitType.GRAM), "g")

    def test_get_type_abbreviation_raises_for_unknown_type(self) -> None:
        class FakeUnitType:
            pass
        with self.assertRaises(ValueError) as context:
            self.product._get_type_abbreviation(FakeUnitType())
        self.assertIn("Tipo de unidade desconhecido", str(context.exception))