# /app/alarming/models.py
import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class AlarmRule(Base):
    __tablename__ = "alarm_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    metric_name = Column(String, nullable=False)
    condition = Column(String, nullable=False)  # e.g., ">", "<", "="
    threshold = Column(Float, nullable=False)
    severity = Column(String, nullable=False, default="warning") # e.g., "warning", "critical"
    is_enabled = Column(Boolean, default=True, nullable=False)

    asset = relationship("Asset", back_populates="alarm_rules")
    alarms = relationship("Alarm", back_populates="rule")

class Alarm(Base):
    __tablename__ = "alarms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id = Column(UUID(as_uuid=True), ForeignKey("alarm_rules.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    triggering_value = Column(Float, nullable=False)
    is_acknowledged = Column(Boolean, default=False, nullable=False)

    rule = relationship("AlarmRule", back_populates="alarms")
