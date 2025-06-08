from logging.config import fileConfig
import os
import sys
from pathlib import Path
from sqlalchemy import engine_from_config, pool
from alembic import context

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.db import Base

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    url = os.getenv('DATABASE_URL')
    if not url:
        raise RuntimeError('DATABASE_URL must be set for migrations')
    return url


def run_migrations_offline():
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        url=get_url(),
        prefix='sqlalchemy.',
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
