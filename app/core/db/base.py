from sqlalchemy.orm import declarative_base

# Se crea una clase Base de la que heredarán todos los modelos de la aplicación.
# Alembic usará el metadata de esta Base para detectar cambios y generar migraciones.
Base = declarative_base()

# Se importan todos los modelos aquí para que Alembic los "vea".
# Gracias a que heredan de Base, se registrarán en los metadatos.
