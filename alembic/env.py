import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# --- 1. Añadir el directorio raíz del proyecto al path de Python ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- 2. Importación de Componentes Clave de la Aplicación ---
from app.core.config import settings
from app.db.base_model import BaseModel
from app.models import *

config = context.config

config.set_main_option('sqlalchemy.url', str(settings.DATABASE_URL))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- 3. Definición del Objetivo para Autogenerate ---
target_metadata = BaseModel.metadata

# El resto del archivo es el boilerplate estándar de Alembic
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
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
