# /app/configuration/models/configuration_parameter.py
"""
Modelo de la base de datos para la entidad ConfigurationParameter.
"""

from sqlalchemy import Column, String, Text, Boolean

from app.db.base_class import Base


class ConfigurationParameter(Base):
    """Modelo SQLAlchemy para un Parámetro de Configuración del Sistema."""
    __tablename__ = "configuration_parameters"

    # La clave del parámetro, ej: "maintenance.preventive.default_days_interval"
    key = Column(String(255), primary_key=True, index=True)
    
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    is_editable = Column(Boolean, default=True, nullable=False)
