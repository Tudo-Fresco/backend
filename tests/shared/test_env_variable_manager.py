from api.shared.env_variable_manager import EnvVariableManager
from unittest.mock import MagicMock, patch
import unittest
import os


class TestEnvVariableManager(unittest.TestCase):

    def setUp(self) -> None:
        self.manager = EnvVariableManager(warn_defaults=True)
        self.manager.logger = MagicMock()

    def test_init_must_set_properties_correctly(self) -> None:
        self.assertTrue(self.manager.warn_defaults)
        self.assertIsInstance(self.manager.logger, MagicMock)
        self.assertIsNone(self.manager.value)

    @patch.dict(os.environ, {'TEST_KEY': 'test_value'})
    def test_load_must_set_value_from_env_variable(self) -> None:
        test_key = 'TEST_KEY'
        test_value = 'test_value'
        result = self.manager.load(test_key)
        self.assertEqual(test_value, self.manager.value)
        self.assertIs(result, self.manager)
        self.manager.logger.log_debug.assert_called_once_with(f'{test_key}: {test_value}')

    @patch.dict(os.environ, {})
    def test_load_must_use_default_when_env_variable_not_found(self) -> None:
        test_key = 'MISSING_KEY'
        default_value = 'default'
        result = self.manager.load(test_key, default_value=default_value)
        self.assertEqual(default_value, self.manager.value)
        self.assertIs(result, self.manager)
        self.manager.logger.log_warning.assert_called_once_with(
            f'Variable {test_key} not found, using default: {default_value}'
        )
        self.manager.logger.log_debug.assert_called_once_with(f'{test_key}: {default_value}')

    @patch.dict(os.environ, {'SECRET_KEY': 'secret'})
    def test_load_must_mask_sensitive_value_in_logs(self) -> None:
        test_key = 'SECRET_KEY'
        test_value = 'secret'
        result = self.manager.load(test_key, is_sensitive=True)
        self.assertEqual(test_value, self.manager.value)
        self.assertIs(result, self.manager)
        self.manager.logger.log_debug.assert_called_once_with(f'{test_key}: [SENSITIVE]')
        self.manager.logger.log_warning.assert_not_called()

    def test_boolean_must_convert_true_correctly(self) -> None:
        self.manager.value = 'true'
        result = self.manager.boolean()
        self.assertTrue(result)

    def test_boolean_must_convert_false_correctly(self) -> None:
        self.manager.value = 'false'
        result = self.manager.boolean()
        self.assertFalse(result)

    def test_boolean_must_raise_when_value_is_none(self) -> None:
        self.manager.value = None
        with self.assertRaises(ValueError) as context:
            self.manager.boolean()
        self.assertEqual('No value loaded to convert to boolean', str(context.exception))

    def test_float_must_convert_valid_float_correctly(self) -> None:
        self.manager.value = '3.14'
        result = self.manager.float()
        self.assertEqual(3.14, result)

    def test_float_must_raise_when_value_is_none(self) -> None:
        self.manager.value = None
        with self.assertRaises(ValueError) as context:
            self.manager.float()
        self.assertEqual('No value loaded to convert to float', str(context.exception))

    def test_float_must_raise_when_value_is_invalid(self) -> None:
        self.manager.value = 'not_a_float'
        with self.assertRaises(ValueError) as context:
            self.manager.float()
        expected_msg = "Cannot convert 'not_a_float' to float: could not convert string to float: 'not_a_float'"
        self.assertEqual(expected_msg, str(context.exception))

    def test_string_must_convert_value_correctly(self) -> None:
        self.manager.value = 42
        result = self.manager.string()
        self.assertEqual('42', result)

    def test_string_must_return_empty_when_value_is_none(self) -> None:
        self.manager.value = None
        result = self.manager.string()
        self.assertEqual('', result)

    def test_integer_must_convert_valid_integer_correctly(self) -> None:
        self.manager.value = '123'
        result = self.manager.integer()
        self.assertEqual(123, result)

    def test_integer_must_raise_when_value_is_none(self) -> None:
        self.manager.value = None
        with self.assertRaises(ValueError) as context:
            self.manager.integer()
        self.assertEqual('No value loaded to convert to integer', str(context.exception))

    def test_integer_must_raise_when_value_is_invalid(self) -> None:
        self.manager.value = 'not_an_int'
        with self.assertRaises(ValueError) as context:
            self.manager.integer()
        expected_msg = "Cannot convert 'not_an_int to integer: invalid literal for int() with base 10: 'not_an_int'"
        self.assertEqual(expected_msg, str(context.exception))

    @patch.dict(os.environ, {})
    def test_set_must_update_environment_and_value(self) -> None:
        test_key = 'NEW_KEY'
        test_value = 'new_value'
        self.manager.set(test_key, test_value)
        self.assertEqual(test_value, os.environ[test_key])
        self.assertEqual(test_value, self.manager.value)
        self.manager.logger.log_debug.assert_called_once_with(f'{test_key}: {test_value}')

    def test_get_raw_must_return_current_value(self) -> None:
        test_value = 'raw_value'
        self.manager.value = test_value
        result = self.manager.get_raw()
        self.assertEqual(test_value, result)

    def test_get_raw_must_return_none_when_no_value(self) -> None:
        self.manager.value = None
        result = self.manager.get_raw()
        self.assertIsNone(result)