# /app/configuration/models/enum_type.py
"""
Modelo de la base de datos para la entidad EnumType.
"""
import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class EnumType(Base):
    """Modelo SQLAlchemy para un Tipo de Enumeración Dinámica."""
    __tablename__ = "enum_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, index=True, nullable=False, comment="Ej: WorkOrderStatus, AssetStatus")
    description = Column(Text, nullable=True)

    # Relación inversa: Un tipo de enum tiene muchos valores.
    values = relationship("EnumValue", back_populates="enum_type", cascade="all, delete-orphan")
