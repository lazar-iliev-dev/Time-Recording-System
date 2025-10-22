# backend/alembic/env.py
from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

# ensure project root is on path so we can import app.models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import models so SQLModel.metadata is populated
# adjust path if your models are elsewhere
from app.models import *  # noqa: F401,F403

config = context.config

# setup logging from config file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# allow DATABASE_URL to be set via env var (recommended)
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
