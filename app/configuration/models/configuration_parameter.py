# /app/configuration/models/configuration_parameter.py
"""
Modelo de la base de datos para la entidad ConfigurationParameter.
"""
import uuid
from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class ConfigurationParameter(Base):
    """Modelo SQLAlchemy para un Parámetro de Configuración del Sistema."""
    __tablename__ = "configuration_parameters"

    # Añadimos ID para consistencia, aunque key sigue siendo única
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # La clave del parámetro, ej: "maintenance.preventive.default_days_interval"
    key = Column(String(255), unique=True, index=True, nullable=False)
    
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    is_editable = Column(Boolean, default=True, nullable=False)
    
    # Soft Delete
    is_active = Column(Boolean, default=True, nullable=False)
