# /app/db/base_model.py (MODIFICADO)

from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr

from app.db.base_class import Base


class BaseModel(Base):
    """
    Clase base para todos los modelos que añade funcionalidades comunes.

    - Hereda de la Base declarativa de SQLAlchemy.
    - Genera automáticamente el `__tablename__` a partir del nombre de la clase.
    - Añade campos `created_at` y `updated_at` automáticos.
    - Se marca como abstracta para que SQLAlchemy no intente crear una tabla para ella.
    """

    __abstract__ = True  # Muy importante: le dice a SQLAlchemy que no cree una tabla "basemodel"

    id: any
    __name__: str

    # --- MEJORA: Añadir timestamps automáticos a todos los modelos ---
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Genera __tablename__ automáticamente en minúsculas y plural (opcional)
    @declared_attr
    def __tablename__(cls) -> str:
        # Ejemplo: la clase "Client" se convierte en la tabla "clients"
        return f"{cls.__name__.lower()}s"
