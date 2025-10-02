# /app/alarming/models/alarm.py
"""
Modelo de la base de datos para la entidad Alarm.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Alarm(Base):
    """Modelo SQLAlchemy para una Alarma activa."""
    __tablename__ = "alarms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relación con la regla que disparó la alarma
    rule_id = Column(UUID(as_uuid=True), ForeignKey("alarm_rules.id"), nullable=False, index=True)
    rule = relationship("AlarmRule", back_populates="alarms")

    # Timestamps del ciclo de vida de la alarma
    triggered_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    cleared_at = Column(DateTime(timezone=True), nullable=True)

    # Estado actual de la alarma
    status = Column(String(50), default="ACTIVE", nullable=False, index=True, comment="ACTIVE, ACKNOWLEDGED, CLEARED")

    # Contexto del disparo
    triggering_value = Column(Float, nullable=False, comment="El valor de la métrica que causó la alerta")
