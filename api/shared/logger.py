from api.enums.log_type import LogType
from termcolor import colored
from datetime import datetime
from typing import Optional


class Logger:
    '''A customizable logging utility with colored output and timestamp support.'''

    DEFAULT_COLORS = {
        LogType.ERROR: 'red',
        LogType.WARNING: 'yellow',
        LogType.DEBUG: 'grey',
        LogType.INFO: 'light_green'
    }

    def __init__(self, who: str) -> None:
        '''Initialize logger with identifier.'''
        self.who = who
        self._api_config = None

    @property
    def api_config(self):
        '''Lazily load ApiConfig singleton on first access.'''
        if self._api_config is None:
            from api.api_config import ApiConfig
            self._api_config = ApiConfig()
        return self._api_config

    @property
    def debug(self) -> bool:
        '''Get debug setting from ApiConfig.'''
        return self.api_config.show_debug

    @property
    def show_timestamp(self) -> bool:
        '''Get timestamp setting from ApiConfig.'''
        return self.api_config.show_timestamp

    def log_error(self, message: str) -> None:
        '''Log an error message with red color.'''
        self._write(LogType.ERROR, message)

    def log_warning(self, message: str) -> None:
        '''Log a warning message with yellow color.'''
        self._write(LogType.WARNING, message)

    def log_debug(self, message: str) -> None:
        '''Log a debug message if debug mode is enabled with grey color.'''
        if self.debug:
            self._write(LogType.DEBUG, message)

    def log_info(self, message: str) -> None:
        '''Log an informational message with light green color.'''
        self._write(LogType.INFO, message)

    def _write(self, log_type: LogType, message: str,
               date_time: Optional[datetime] = None) -> None:
        '''Internal method to handle message composition and output.'''
        composed_message = self._compose_log_message(log_type, message, date_time)
        color = self.DEFAULT_COLORS[log_type]
        colored_message = colored(composed_message, color)
        print(colored_message)

    def _compose_log_message(self, log_type: LogType, message: str, date_time: Optional[datetime] = None) -> str:
        '''Compose a formatted log message with optional timestamp.'''
        if date_time is None:
            date_time = datetime.now()
        if self.show_timestamp:
            timestamp = date_time.isoformat()
            log_parts = [timestamp, log_type.value, self.who, message]
            separator = '|'
            formatted_message = separator.join(log_parts[:-1])
            formatted_message = formatted_message + '> ' + message
        else:
            log_parts = [log_type.value, self.who, message]
            separator = '|'
            formatted_message = separator.join(log_parts[:-1])
            formatted_message = formatted_message + '> ' + message
        return formatted_message