from api.exceptions.validation_exception import ValidationException
from api.domain.product_name import ProductName
from tests.helper.text_generator import TextGenerator
import unittest


class TestProductName(unittest.TestCase):

    def test_validate_must_pass_for_all_properties(self) -> None:
        expected_product_name = 'Banana'
        product = ProductName(name=expected_product_name)
        product.validate()
        self.assertEqual(expected_product_name, product.name)

    def test_validate_must_not_raise_validation_exception_when_name_length_is_equal_to_the_limit(self) -> None:
        text_generator = TextGenerator()
        expected_product_name = text_generator.generate_random_text(length=256)
        product = ProductName(name=expected_product_name)
        product.validate()
        self.assertEqual(expected_product_name, product.name)

    def test_validate_must_raise_validation_exception_when_name_length_is_greater_than_limit(self) -> None:
        text_generator = TextGenerator()
        expected_product_name = text_generator.generate_random_text(length=257)
        product = ProductName(name=expected_product_name)
        with self.assertRaises(ValidationException) as context:
            product.validate()
        self.assertEqual('Nome do produto: Deve ser menor do que 256 caracters.\n', context.exception.message)