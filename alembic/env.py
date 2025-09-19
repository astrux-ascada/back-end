
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Importa la clase Base de tus modelos de SQLAlchemy.
# Asumiremos que estará en core.db.base. ¡Tendremos que crear este archivo!
from app.core.db.base import Base

# --- ¡AÑADIR ESTO PARA AUTOGENERATE! ---
# Importa tus modelos aquí para que Alembic los detecte.
from app.core.models.assets import Asset  # noqa
from app.core.models.maintenance import MaintenanceOrder, SparePart  # noqa
from app.core.models.identity import User  # noqa

# Este es el objeto de configuración de Alembic, que da acceso a los
# valores del archivo .ini.
config = context.config

# Interpreta el archivo de configuración para el logging de Python.
# Esta línea básicamente configura los loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Añade aquí tu metadato de modelo para el soporte de 'autogenerate'.
# Por ejemplo:
# target_metadata = my_model.Base.metadata
target_metadata = Base.metadata

# otros valores desde la config, definidos por las necesidades de env.py,
# se pueden obtener con:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'.

    Esto configura el contexto solo con una URL
    y no con un Engine, aunque un Engine es aceptable
    aquí también. Al omitir la creación del Engine,
    ni siquiera necesitamos que un DBAPI esté disponible.

    Las llamadas a context.execute() emiten la cadena dada a la
    salida del script.

    """
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
    """Ejecuta migraciones en modo 'online'.

    En este escenario necesitamos crear un Engine
    y asociar una conexión con el contexto.

    """
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
