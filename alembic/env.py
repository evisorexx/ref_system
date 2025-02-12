import os
from dotenv import load_dotenv
from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine
from referral_system.database.session import Base
from referral_system.models.referral_code import *
from referral_system.models.user import *

load_dotenv()

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
target_metadata = Base.metadata
print(target_metadata)


def get_database_url():
    database_url = 'postgresql' + os.getenv("DATABASE_URL")
    print(f'Migrating to URL: {database_url}')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return database_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(get_database_url)

    with engine.connect() as connection:
        context.configure(
                    connection=connection,
                    target_metadata=target_metadata
                    )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
