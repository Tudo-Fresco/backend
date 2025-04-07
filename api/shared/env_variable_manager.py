from typing import Any, Optional
from api.shared.logger import Logger
from dotenv import load_dotenv
import os


class EnvVariableManager:
    '''Manages environment variables with type conversion and logging capabilities.'''
    
    def __init__(self, warn_defaults: bool = True) -> None:
        '''Initialize the environment variable manager with logging and warning settings.'''
        load_dotenv()
        self.warn_defaults = warn_defaults
        self.logger = Logger('EnvVariableManager')
        self.value = None
    
    def load(self, variable_name: str, default_value: Any = None, 
             is_sensitive: bool = False) -> 'EnvVariableManager':
        '''
        Load an environment variable with optional default and sensitivity handling.
        
        Args:
            variable_name: Name of the environment variable to load
            default_value: Value to use if variable is not found
            is_sensitive: If True, masks the value in logs
            
        Returns:
            Self for method chaining
        '''
        self.value = os.getenv(variable_name)
        if self.value is None:
            self.value = default_value
            if self.warn_defaults:
                default_value_str = str(default_value) if default_value is not None else 'None'
                warning_msg = f'Variable {variable_name} not found, using default: {default_value_str}'
                self.logger.log_warning(warning_msg)
        self._log_variable(variable_name, is_sensitive)
        return self
    
    def boolean(self) -> bool:
        '''Convert the current value to a boolean.'''
        if self.value is None:
            raise ValueError('No value loaded to convert to boolean')
        result = str(self.value).lower() == 'true'
        return result
    
    def float(self) -> float:
        '''Convert the current value to a float.'''
        if self.value is None:
            raise ValueError('No value loaded to convert to float')
        try:
            result = float(self.value)
            return result
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert '{self.value}' to float: {str(e)}")
    
    def string(self) -> str:
        '''Convert the current value to a string.'''
        if self.value is None:
            return ''
        result = str(self.value)
        return result
    
    def integer(self) -> int:
        '''Convert the current value to an integer.'''
        if self.value is None:
            raise ValueError('No value loaded to convert to integer')
        try:
            result = int(self.value)
            return result
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert '{self.value} to integer: {str(e)}")

    def _log_variable(self, variable_name: str, is_sensitive: bool = False) -> None:
        '''Log the loaded variable value, masking if sensitive.'''
        if is_sensitive:
            debug_msg = f'{variable_name}: [SENSITIVE]'
            self.logger.log_debug(debug_msg)
        else:
            debug_msg = f'{variable_name}: {str(self.value)}'
            self.logger.log_debug(debug_msg)
    
    def set(self, variable_name: str, value: Any) -> None:
        '''Set an environment variable with the given value.'''
        string_value = str(value)
        os.environ[variable_name] = string_value
        self.value = string_value
        self._log_variable(variable_name, is_sensitive=False)

    def get_raw(self) -> Optional[Any]:
        '''Return the current raw value without conversion.'''
        return self.value