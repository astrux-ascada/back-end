
import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Importa la clase Base de tus modelos de SQLAlchemy.
from app.core.db.base import Base

# --- ¡AÑADIR ESTO PARA AUTOGENERATE! ---
# Importa tus modelos aquí para que Alembic los detecte.
from app.core.models.assets import Asset  # noqa
from app.core.models.maintenance import MaintenanceOrder, SparePart  # noqa
from app.core.models.identity import User, Role  # noqa
from app.core.models.plant import Section  # noqa

# Este es el objeto de configuración de Alembic, que da acceso a los
# valores del archivo .ini.
config = context.config

# --- CONFIGURACIÓN DE LA URL DE LA BASE DE DATOS CON VARIABLES DE ENTORNO ---

# Lee las credenciales de las variables de entorno.
# Los valores por defecto están optimizados para el entorno Docker.
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "IndustrialSecreto2025!")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "industrial_orchestrator")

# Construye la URL de la base de datos
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Establece la URL en la configuración de Alembic
config.set_main_option("sqlalchemy.url", DATABASE_URL)


# Interpreta el archivo de configuración para el logging de Python.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Añade aquí tu metadato de modelo para el soporte de 'autogenerate'.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online'."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
