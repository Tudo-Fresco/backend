from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi import APIRouter
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import make_url
from sqlalchemy.ext .asyncio.engine import AsyncEngine
# Controllers
from api.controllers.address_controller import AddressController
from api.controllers.auth_controller import AuthController
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.demand_controller import DemandController
from api.controllers.product_controller import ProductController
from api.controllers.reel_controller import ReelController
from api.controllers.store_controller import StoreController
from api.controllers.user_controller import UserController

# Repositories
from api.infrastructure.repositories.address_repository import AddressRepository
from api.infrastructure.repositories.demand_repository import DemandRepository
from api.infrastructure.repositories.product_repository import ProductRepository
from api.infrastructure.repositories.store_repository import StoreRepository
from api.infrastructure.repositories.user_repository import UserRepository

# Services
from api.services.address_service import AddressService
from api.services.auth_service import AuthService
from api.services.demand_service import DemandService
from api.services.product_service import ProductService
from api.services.reel_service import ReelService
from api.services.store_service import StoreService
from api.services.user_service import UserService

# Config
from api.api_config import ApiConfig
from api.shared.env_variable_manager import EnvVariableManager
from api.shared.logger import Logger


class ApiRouterBuilder:
    def __init__(self):
        ApiConfig()
        self.logger = Logger(self.__class__.__name__)
        self.logger.log_info('Initializing AppRouterBuilder')
        self.env = EnvVariableManager()
        db_url = self.env.load('DB_URL', is_sensitive=True).string()
        self.engine = self.__create_sql_engine(db_url)
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)

    def build(self) -> list[APIRouter]:
        self.logger.log_info('Building API routers')
        routers = []
        session = self.sessionmaker()

        # User
        self.logger.log_debug('Creating UserRepository, UserService, and UserController')
        user_repository = UserRepository(session)
        user_service = UserService(user_repository)
        
        #Auth
        auth_service = AuthService(user_service)
        auth_controller = AuthController(auth_service)
        routers.append(auth_controller.router)
        auth_wrapper = AuthWrapper(auth_service)

        user_controller = UserController(user_service, auth_wrapper)
        routers.append(user_controller.router)

        # Address
        self.logger.log_debug('Creating AddressRepository, AddressService, and AddressController')
        address_repository = AddressRepository(session)
        address_service = AddressService(address_repository)
        address_controller = AddressController(address_service, auth_wrapper)
        routers.append(address_controller.router)

        # Store
        self.logger.log_debug('Creating StoreRepository, StoreService, and StoreController')
        store_repository = StoreRepository(session)
        store_service = StoreService(store_repository, user_repository, address_repository)
        store_controller = StoreController(store_service, auth_wrapper)
        routers.append(store_controller.router)

        # Product
        self.logger.log_debug('Creating ProductRepository, ProductService, and ProductController')
        product_repository = ProductRepository(session)
        product_service = ProductService(product_repository)
        product_controller = ProductController(product_service, auth_wrapper)
        routers.append(product_controller.router)

        # Demand
        self.logger.log_debug('Creating DemandRepository, DemandService, and DemandController')
        demand_repository = DemandRepository(session)
        demand_service = DemandService(
            demand_repository,
            store_repository,
            product_repository,
            user_repository,
            product_service
        )
        demand_controller = DemandController(demand_service, auth_wrapper)
        routers.append(demand_controller.router)

        #Reel
        self.logger.log_debug('Creating ReelService and ReelController')
        reel_service = ReelService(demand_service)
        reel_controller = ReelController(reel_service, auth_wrapper)
        routers.append(reel_controller.router)

        self.logger.log_info('All routers successfully initialized')
        return routers

    def __create_sql_engine(self, db_connection_url: str) -> AsyncEngine:
        self.logger.log_info('Creating database engine')
        is_local = self.env.load('IS_LOCAL', default_value=False).boolean()
        if is_local:
            self.logger.log_info('Creating the engine for local environment')
            return create_async_engine(db_connection_url, echo=False)
        self.logger.log_info('Creating the engine for Google Cloud environment')
        cloud_connection_name = self.env.load('CLOUD_SQL_CONNECTION_NAME').string()
        parsed_url = make_url(db_connection_url)
        db_user = parsed_url.username
        db_password = parsed_url.password
        db_name = parsed_url.database
        socket_path = f'/cloudsql/{cloud_connection_name}'
        db_url = URL.create(
            drivername='postgresql+asyncpg',
            username=db_user,
            password=db_password,
            database=db_name,
            query={'host': socket_path}
        )
        engine = create_async_engine(db_url, echo=False)
        self.logger.log_info('The database engine was successfully created')
        return engine