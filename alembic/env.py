import os
import asyncio
from dotenv import load_dotenv
from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from referral_system.database.session import Base

load_dotenv()

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def get_database_url():
    database_url = os.getenv("DATABASE_URL")
    print(f'Migrating to URL: {database_url}')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return database_url


def run_migrations_online():
    connectable = create_async_engine(
        get_database_url(),
        poolclass=pool.NullPool,
    )

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_async_migrations())


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

run_migrations_online()