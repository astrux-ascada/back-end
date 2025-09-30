# /app/identity/models/user_sector_association.py
"""
Tabla de asociación para la relación muchos-a-muchos entre User y Sector.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class UserSectorAssociation(Base):
    """Modelo de la tabla de asociación que vincula Usuarios con Sectores."""
    __tablename__ = "user_sectors"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    sector_id = Column(UUID(as_uuid=True), ForeignKey("sectors.id"), primary_key=True)
