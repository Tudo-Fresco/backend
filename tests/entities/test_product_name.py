from unittest.mock import MagicMock, patch
from api.exceptions.validation_exception import ValidationException
from api.domain.product_name import ProductName
from tests.helper.text_generator import TextGenerator
from freezegun import freeze_time
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
        self.assertEqual(expected_product_name, product.name)
    
    @freeze_time('2025-03-06 12:00:00')
    @patch('api.domain.base_entity.uuid4', return_value='123e4567-e89b-12d3-a456-426614174000', autospec=True)
    def test_to_dict_must_convert_to_dict_correctly(self, mock_uuid: MagicMock) -> None:
        expected_uuid = mock_uuid.return_value 
        expected_product_name = 'Maçã'
        expected_dict: dict = {
            'name': expected_product_name,
            'uuid': expected_uuid,
            'created_at': '2025-03-06T12:00:00+00:00',
            'updated_at': '2025-03-06T12:00:00+00:00',
            'active': True
        }
        product = ProductName(name=expected_product_name)
        result = product.to_dict()
        self.assertDictEqual(expected_dict, result)
        self.assertEqual(expected_product_name, product.name)

    def test_active_must_activate_correctly(self) -> None:
        instance_dict: dict = {
            'name': 'Pimentão',
            'uuid': '123e4567-e89b-12d3-a456-426614174000',
            'created_at': '2025-03-06T12:00:00+00:00',
            'updated_at': '2025-03-06T12:00:00+00:00',
            'active': False
        }
        product_name = ProductName(**instance_dict)
        self.assertFalse(product_name.active)
        product_name.activate()
        self.assertTrue(product_name.active)
        self.assertNotEqual(instance_dict.get('updated_at'), product_name.updated_at.isoformat())

    def test_dactivate_must_deactivate_correctly(self) -> None:
        instance_dict: dict = {
            'name': 'Pimentão',
            'uuid': '123e4567-e89b-12d3-a456-426614174000',
            'created_at': '2025-03-06T12:00:00+00:00',
            'updated_at': '2025-03-06T12:00:00+00:00',
            'active': True
        }
        product_name = ProductName(**instance_dict)
        self.assertTrue(product_name.active)
        product_name.deactivate()
        self.assertFalse(product_name.active)
        self.assertNotEqual(instance_dict.get('updated_at'), product_name.updated_at.isoformat())