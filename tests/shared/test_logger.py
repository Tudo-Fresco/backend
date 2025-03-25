from unittest.mock import MagicMock, patch
from termcolor import colored
from api.shared.logger import Logger
from api.enums.log_type import LogType
from freezegun import freeze_time
import unittest


class TestLogger(unittest.TestCase):

    def setUp(self) -> None:
        '''Set up a fresh Logger instance for each test.'''
        self.logger = Logger(who='TestApp')
        self.logger._api_config = MagicMock()
        self.logger._api_config.show_debug = False
        self.logger._api_config.show_timestamp = False
        self.logger._api_config.env_mgr = MagicMock()

    def test_debug_property_must_reflect_api_config(self) -> None:
        self.logger._api_config.show_debug = True
        self.assertTrue(self.logger.debug)
        self.logger._api_config.show_debug = False
        self.assertFalse(self.logger.debug)

    def test_show_timestamp_property_must_reflect_api_config(self) -> None:
        self.logger._api_config.show_timestamp = True
        self.assertTrue(self.logger.show_timestamp)
        self.logger._api_config.show_timestamp = False
        self.assertFalse(self.logger.show_timestamp)

    @patch('builtins.print')
    def test_log_error_must_print_with_red_color(self, mock_print: MagicMock) -> None:
        message = 'Error occurred'
        self.logger.log_error(message)
        expected_message = f'ERROR|TestApp> {message}'
        mock_print.assert_called_once_with(colored(expected_message, 'red'))

    @patch('builtins.print')
    def test_log_warning_must_print_with_yellow_color(self, mock_print: MagicMock) -> None:
        message = 'Warning issued'
        self.logger.log_warning(message)
        expected_message = f'WARNING|TestApp> {message}'
        mock_print.assert_called_once_with(colored(expected_message, 'yellow'))

    @patch('builtins.print')
    def test_log_debug_must_print_when_debug_enabled(self, mock_print: MagicMock) -> None:
        self.logger._api_config.show_debug = True
        message = 'Debug info'
        self.logger.log_debug(message)
        expected_message = f'DEBUG|TestApp> {message}'
        mock_print.assert_called_once_with(colored(expected_message, 'grey'))

    @patch('builtins.print')
    def test_log_debug_must_not_print_when_debug_disabled(self, mock_print: MagicMock) -> None:
        self.logger._api_config.show_debug = False
        message = 'Debug info'
        self.logger.log_debug(message)
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_log_info_must_print_with_light_green_color(self, mock_print: MagicMock) -> None:
        message = 'Info message'
        self.logger.log_info(message)
        expected_message = f'INFO|TestApp> {message}'
        mock_print.assert_called_once_with(colored(expected_message, 'light_green'))

    @freeze_time('2025-03-24 12:00:00')
    @patch('builtins.print')
    def test_write_must_include_timestamp_when_enabled(self, mock_print: MagicMock) -> None:
        self.logger._api_config.show_timestamp = True
        message = 'Timestamped message'
        self.logger._write(LogType.INFO, message)
        expected_message = f'2025-03-24T12:00:00|INFO|TestApp> {message}'
        mock_print.assert_called_once_with(colored(expected_message, 'light_green'))

    @patch('builtins.print')
    def test_write_must_exclude_timestamp_when_disabled(self, mock_print: MagicMock) -> None:
        self.logger._api_config.show_timestamp = False
        message = 'No timestamp message'
        self.logger._write(LogType.INFO, message)
        expected_message = f'INFO|TestApp> {message}'
        mock_print.assert_called_once_with(colored(expected_message, 'light_green'))

    @freeze_time('2025-03-24 12:00:00')
    def test_compose_log_message_must_include_timestamp_when_enabled(self) -> None:
        self.logger._api_config.show_timestamp = True
        message = 'Test message'
        result = self.logger._compose_log_message(LogType.INFO, message)
        expected_message = f'2025-03-24T12:00:00|INFO|TestApp> {message}'
        self.assertEqual(expected_message, result)

    def test_compose_log_message_must_exclude_timestamp_when_disabled(self) -> None:
        self.logger._api_config.show_timestamp = False
        message = 'Test message'
        result = self.logger._compose_log_message(LogType.INFO, message)
        expected_message = f'INFO|TestApp> {message}'
        self.assertEqual(expected_message, result)