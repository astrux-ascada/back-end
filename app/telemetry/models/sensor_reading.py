# /app/telemetry/models/sensor_reading.py
"""
Modelo de la base de datos para la entidad SensorReading.

Esta tabla está diseñada para ser una Hypertable de TimescaleDB, optimizada
para almacenar grandes volúmenes de datos de series temporales.
"""

from sqlalchemy import Column, String, func, TIMESTAMP, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class SensorReading(Base):
    """Modelo SQLAlchemy para una Lectura de Sensor (Telemetría)."""
    __tablename__ = "sensor_readings"

    # --- Clave Primaria Compuesta ---
    # La combinación de cuándo y de qué activo es única.
    timestamp = Column(TIMESTAMP(timezone=True), primary_key=True, index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), primary_key=True)

    # --- Datos de la Métrica ---
    metric_name = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)

    # --- Relación con Asset ---
    # Permite acceder al objeto Asset desde una lectura de sensor.
    asset = relationship("Asset")
