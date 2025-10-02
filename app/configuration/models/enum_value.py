# /app/configuration/models/enum_value.py
"""
Modelo de la base de datos para la entidad EnumValue.
"""
import uuid

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class EnumValue(Base):
    """Modelo SQLAlchemy para un Valor de Enumeración Dinámica."""
    __tablename__ = "enum_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Relación con el tipo de enum al que pertenece
    enum_type_id = Column(UUID(as_uuid=True), ForeignKey("enum_types.id"), nullable=False, index=True)
    enum_type = relationship("EnumType", back_populates="values")

    value = Column(String(100), nullable=False, comment="El valor real, ej: IN_PROGRESS")
    label = Column(String(150), nullable=False, comment="La etiqueta para la UI, ej: En Progreso")
    color = Column(String(20), nullable=True, comment="Un color opcional para la UI, ej: #3b82f6")
