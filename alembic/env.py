from logging.config import fileConfig
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.database import Base
from app.core.settings import get_settings

# Import All Models Here
from app.auth.models import *
from app.product.models import Product
from app.cart.models import Cart
from app.orders.models import Order
from app.orders.models import OrderItem



# Load settings and database URL
settings = get_settings()




# Alembic Config
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URI.replace("%", "%%"))

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set metadata for 'autogenerate'
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
