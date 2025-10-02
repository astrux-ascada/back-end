# /app/alarming/models/alarm_rule.py
"""
Modelo de la base de datos para la entidad AlarmRule.
"""
import uuid

from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AlarmRule(Base):
    """Modelo SQLAlchemy para una Regla de Alerta."""
    __tablename__ = "alarm_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relación con el activo al que se aplica la regla
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    asset = relationship("Asset")

    metric_name = Column(String(100), nullable=False, index=True, comment="Ej: temperature_celsius")
    condition = Column(String(10), nullable=False, comment="Ej: >, <, ==")
    threshold = Column(Float, nullable=False)
    severity = Column(String(50), nullable=False, index=True, comment="INFO, WARNING, CRITICAL")
    is_enabled = Column(Boolean, default=True, nullable=False, index=True)

    # Relación inversa: Una regla puede disparar muchas alarmas.
    alarms = relationship("Alarm", back_populates="rule", cascade="all, delete-orphan")
