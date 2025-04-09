import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from api.shared.logger import Logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.shared.env_variable_manager import EnvVariableManager
env = EnvVariableManager()
async_db_url = env.load('DB_URL', is_sensitive=True).string()
logger = Logger('Alembic')
from api.infrastructure.models.user_model import UserModel
from api.infrastructure.models.address_model import AddressModel
from api.infrastructure.models.demand_model import DemandModel
from api.infrastructure.models.product_model import ProductModel
from api.infrastructure.models.store_model import StoreModel
from api.infrastructure.models import base_model
target_metadata = base_model.Base.metadata
logger.log_info(str(base_model.Base.metadata.tables.keys()))

config = context.config
config.set_main_option("sqlalchemy.url", async_db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=async_db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(async_db_url, pool_pre_ping=True)

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(
                lambda sync_conn: context.configure(
                    connection=sync_conn,
                    target_metadata=target_metadata,
                    compare_type=True,
                )
            )
            async with connection.begin():
                await connection.run_sync(lambda sync_conn: context.run_migrations())

    asyncio.run(do_run_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
