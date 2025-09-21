# /app/core_engine/models/data_source.py
"""
Modelo de la base de datos para la entidad DataSource.

Representa la configuración de una fuente de datos externa, como un PLC,
un gateway OPC UA o un broker MQTT.
"""
import uuid

from sqlalchemy import Column, String, func, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.base_class import Base


class DataSource(Base):
    """Modelo SQLAlchemy para una Fuente de Datos."""
    __tablename__ = "data_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(100), unique=True, index=True, nullable=False, comment="Nombre descriptivo, ej: 'PLC Línea de Ensamblaje 3'")
    protocol = Column(String(50), nullable=False, index=True, comment="Protocolo de comunicación, ej: 'OPCUA', 'MODBUS_TCP'")
    
    # Campo JSON para almacenar parámetros de conexión flexibles.
    # Ej: {"host": "192.168.1.10", "port": 4840, "security_mode": "SignAndEncrypt"}
    connection_params = Column(JSONB, nullable=False)

    is_active = Column(Boolean, default=False, nullable=False, index=True, comment="Habilita o deshabilita la recolección de datos de esta fuente.")
    description = Column(String(255), nullable=True)

    # --- Campos de Auditoría ---
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
