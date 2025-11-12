from __future__ import annotations
from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Engine, Connection, create_engine
from app.core.settings import settings
from app.db.base import Base  # importa tus modelos en base.py
import os

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_sync_url() -> str:
    return settings.DATABASE_URL_SYNC

def run_migrations_offline() -> None:
    url = get_sync_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable: Engine = create_engine(get_sync_url(), poolclass=pool.NullPool, future=True)
    with connectable.connect() as connection:  # type: Connection
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
