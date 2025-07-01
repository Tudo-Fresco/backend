from typing import AsyncGenerator
from fastapi import APIRouter, Depends
from api.utils.session_factory import SessionFactory
from api.utils.repository_factory import RepositoryFactory
from api.infrastructure.repositories.address_repository import AddressRepository
from api.infrastructure.repositories.demand_repository import DemandRepository
from api.infrastructure.repositories.product_repository import ProductRepository
from api.infrastructure.repositories.store_repository import StoreRepository
from api.infrastructure.repositories.user_repository import UserRepository
from api.services.address_service import AddressService
from api.services.auth_service import AuthService
from api.services.demand_service import DemandService
from api.services.product_service import ProductService
from api.services.reel_service import ReelService
from api.services.store_service import StoreService
from api.services.user_service import UserService
from api.controllers.address_controller import AddressController
from api.controllers.auth_controller import AuthController
from api.controllers.auth_wrapper import AuthWrapper
from api.controllers.demand_controller import DemandController
from api.controllers.product_controller import ProductController
from api.controllers.reel_controller import ReelController
from api.controllers.store_controller import StoreController
from api.controllers.user_controller import UserController
from api.shared.logger import Logger
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
import asyncio


class ApiRouterBuilder:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.logger.log_info("Initializing ApiRouterBuilder")
        self.session_factory = SessionFactory()
        self.repository_factory = RepositoryFactory()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async for session in self.session_factory.get_session():
            yield session

    def get_repository(self, repo_class, session: AsyncSession):
        return self.repository_factory.get_repository(repo_class, session)

    def build(self) -> list[APIRouter]:
        self.logger.log_info("Building API routers")
        routers = []
        Depends(lambda session=Depends(self.get_session): self.get_repository(UserRepository, session))
        Depends(lambda session=Depends(self.get_session): self.get_repository(AddressRepository, session))
        Depends(lambda session=Depends(self.get_session): self.get_repository(StoreRepository, session))
        Depends(lambda session=Depends(self.get_session): self.get_repository(ProductRepository, session))
        Depends(lambda session=Depends(self.get_session): self.get_repository(DemandRepository, session))

        session = asyncio.run(self.session_factory.async_session_maker().__aenter__())

        # Create repositories
        user_repository = UserRepository(session)
        address_repository = AddressRepository(session)
        store_repository = StoreRepository(session)
        product_repository = ProductRepository(session)
        demand_repository = DemandRepository(session)

        # Services
        user_service = UserService(user_repository)
        auth_service = AuthService(user_service)
        auth_wrapper = AuthWrapper(auth_service)
        address_service = AddressService(address_repository)
        store_service = StoreService(store_repository, user_repository, address_repository)
        product_service = ProductService(product_repository)
        demand_service = DemandService(demand_repository, store_repository, product_repository, user_repository, product_service)
        reel_service = ReelService(demand_service)

        # Controllers
        auth_controller = AuthController(auth_service)
        user_controller = UserController(user_service, auth_wrapper)
        address_controller = AddressController(address_service, auth_wrapper)
        store_controller = StoreController(store_service, auth_wrapper)
        product_controller = ProductController(product_service, auth_wrapper)
        demand_controller = DemandController(demand_service, auth_wrapper)
        reel_controller = ReelController(reel_service, auth_wrapper)

        # Append routers
        routers.extend([
            auth_controller.router,
            user_controller.router,
            address_controller.router,
            store_controller.router,
            product_controller.router,
            demand_controller.router,
            reel_controller.router
        ])

        self.logger.log_info("All routers successfully initialized")
        return routers
