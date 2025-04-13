from enum import Enum


class LogType(Enum):
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    DEBUG = 'DEBUG'
    INFO = 'INFO'