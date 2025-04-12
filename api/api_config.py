from api.shared.env_variable_manager import EnvVariableManager


class ApiConfig:
    '''Singleton class to manage application-wide environment variables.'''
    
    _instance = None
    
    def __new__(cls) -> 'ApiConfig':
        '''Ensure only one instance exists.'''
        if cls._instance is None:
            cls._instance = super(ApiConfig, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        '''Initialize configuration values from environment variables.'''
        self.show_debug = False
        self.show_timestamp = False
        self.env_mgr = EnvVariableManager(warn_defaults=True)
        self.show_debug: bool = self.env_mgr.load('SHOW_DEBUG_LOGS', default_value='false').boolean()
        self.show_timestamp: bool = self.env_mgr.load('SHOW_TIMESTAMPED_LOGS', default_value='false').boolean()