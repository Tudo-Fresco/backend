from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import make_url
from api.shared.env_variable_manager import EnvVariableManager
from api.shared.logger import Logger


class SessionFactory:
    def __init__(self):
        self.env = EnvVariableManager()
        self.logger = Logger('SessionFactory')
        self.db_url = self.env.load('DB_URL', is_sensitive=True).string()
        self.engine = self.__create_sql_engine(self.db_url)
        self.async_session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

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
