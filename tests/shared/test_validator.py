from api.exceptions.validation_exception import ValidationException
from api.shared.validator import Validator
import unittest


class TestValidator(unittest.TestCase):

    def setUp(self) -> None:
        """Set up a fresh Validator instance for each test."""
        self.validator = Validator()

    def test_on_must_set_value_and_field_name_correctly(self) -> None:
        expected_value = "test_value"
        expected_field_name = "test_field"
        result = self.validator.on(expected_value, expected_field_name)
        self.assertEqual(expected_value, self.validator.value)
        self.assertEqual(expected_field_name, self.validator.field_name)
        self.assertIs(result, self.validator)

    def test_character_limit_must_pass_when_within_limit(self) -> None:
        test_value = "abc"
        self.validator.on(test_value, "field").character_limit(5)
        self.assertEqual([], self.validator.current_field_errors)

    def test_character_limit_must_fail_when_exceeds_limit(self) -> None:
        test_value = "abcdef"
        self.validator.on(test_value, "field").character_limit(5)
        expected_error = "field: Value must be smaller than 5 characters.\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_not_empty_must_pass_when_value_present(self) -> None:
        test_value = "something"
        self.validator.on(test_value, "field").not_empty()
        self.assertEqual([], self.validator.current_field_errors)

    def test_not_empty_must_fail_when_value_empty(self) -> None:
        test_value = ""
        self.validator.on(test_value, "field").not_empty()
        expected_error = "field: Value cannot be empty.\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_greater_or_equal_must_pass_when_equal(self) -> None:
        test_value = 10
        self.validator.on(test_value, "field").greater_or_equal(10)
        self.assertEqual([], self.validator.current_field_errors)

    def test_greater_or_equal_must_fail_when_less(self) -> None:
        test_value = 5
        self.validator.on(test_value, "field").greater_or_equal(10)
        expected_error = "field: Value must be greater or equal than 10\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_greater_must_pass_when_greater(self) -> None:
        test_value = 11
        self.validator.on(test_value, "field").greater_or_equal(10)
        self.assertEqual([], self.validator.current_field_errors)

    def test_greater_must_fail_when_less(self) -> None:
        test_value = 9
        self.validator.on(test_value, "field").greater(10)
        expected_error = "field: Value must be greater than 10\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_greater_must_fail_when_equal(self) -> None:
        test_value = 5
        self.validator.on(test_value, "field").greater(5)
        expected_error = "field: Value must be greater than 5\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_smaller_or_equal_must_pass_when_smaller(self) -> None:
        test_value = 9
        self.validator.on(test_value, "field").smaller_or_equal(10)
        self.assertEqual([], self.validator.current_field_errors)

    def test_smaller_or_equal_must_pass_when_equal(self) -> None:
        test_value = 10
        self.validator.on(test_value, "field").smaller_or_equal(10)
        self.assertEqual([], self.validator.current_field_errors)

    def test_smaller_or_equal_must_fail_when_greater(self) -> None:
        test_value = 15
        self.validator.on(test_value, "field").smaller_or_equal(10)
        expected_error = "field: Value must be smaller or equal than 10\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_smaller_must_pass_when_smaller(self) -> None:
        test_value = 9
        self.validator.on(test_value, "field").smaller(10)
        self.assertEqual([], self.validator.current_field_errors)

    def test_smaller_must_fail_when_greater(self) -> None:
        test_value = 9
        self.validator.on(test_value, "field").smaller(8)
        expected_error = "field: Value must be smaller than 8\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_smaller_must_fail_when_equal(self) -> None:
        test_value = 5
        self.validator.on(test_value, "field").smaller(5)
        expected_error = "field: Value must be smaller than 5\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_cnpj_is_valid_must_pass_when_valid(self) -> None:
        test_value = "12.345.678/0001-95"
        self.validator.on(test_value, "cnpj").cnpj_is_valid()
        self.assertEqual([], self.validator.current_field_errors)

    def test_cnpj_is_valid_must_fail_when_invalid(self) -> None:
        test_value = "invalid_cnpj"
        self.validator.on(test_value, "cnpj").cnpj_is_valid()
        expected_error = f"cnpj: {test_value} is not a valid Cnpj\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_cpf_is_valid_must_pass_when_valid(self) -> None:
        test_value = "123.456.789-09"
        self.validator.on(test_value, "cpf").cpf_is_valid()
        self.assertEqual([], self.validator.current_field_errors)

    def test_cpf_is_valid_must_fail_when_invalid(self) -> None:
        test_value = "invalid_cpf"
        self.validator.on(test_value, "cpf").cpf_is_valid()
        expected_error = f"cpf: {test_value} is not a valid Cpf\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_url_is_valid_must_pass_when_valid(self) -> None:
        test_value = "https://example.com"
        self.validator.on(test_value, "url").url_is_valid()
        self.assertEqual([], self.validator.current_field_errors)

    def test_url_is_valid_must_fail_when_no_scheme(self) -> None:
        test_value = "example.com"
        self.validator.on(test_value, "url").url_is_valid()
        expected_error = "url: URL must have a scheme (e.g., http:// or https://)\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_url_is_valid_must_fail_when_no_domain(self) -> None:
        test_value = "https://"
        self.validator.on(test_value, "url").url_is_valid()
        expected_error = "url: URL must have a domain (e.g., example.com)\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_url_is_valid_must_fail_when_not_string(self) -> None:
        test_value = 123
        self.validator.on(test_value, "url").url_is_valid()
        expected_error = "url: URL must be a string\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_url_is_valid_must_fail_when_empty(self) -> None:
        test_value = ""
        self.validator.on(test_value, "url").url_is_valid()
        expected_error = "url: URL cannot be empty\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_with_message_must_override_last_error(self) -> None:
        test_value = ""
        self.validator.on(test_value, "field").not_empty().with_message("Custom empty error")
        expected_error = "field: Custom empty error\n"
        with self.assertRaises(ValidationException) as context:
            self.validator.check()
        self.assertEqual(expected_error, context.exception.message)

    def test_check_must_clear_errors_after_raising(self) -> None:
        test_value = ""
        self.validator.on(test_value, "field").not_empty()
        with self.assertRaises(ValidationException):
            self.validator.check()
        self.assertEqual([], self.validator.current_field_errors)

    def test_check_must_not_raise_when_no_errors(self) -> None:
        test_value = "valid"
        self.validator.on(test_value, "field").not_empty()
        result = self.validator.check()
        self.assertIsNone(result)
        self.assertEqual([], self.validator.current_field_errors)