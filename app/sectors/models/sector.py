# /app/sectors/models/sector.py
"""
Modelo de la base de datos para la entidad Sector.

Representa un área física o lógica dentro de la planta.
"""
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Sector(Base):
    """Modelo SQLAlchemy para un Sector de la planta."""
    __tablename__ = "sectors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

    # Las relaciones `users` y `assets` se definirán en los __init__.py de los módulos correspondientes
    # para evitar problemas de importación circular.
