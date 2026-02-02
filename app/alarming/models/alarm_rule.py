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
    __tablename__ = "alarm_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    metric_name = Column(String, nullable=False)
    condition = Column(String, nullable=False)  # e.g., '>', '<', '=='
    threshold = Column(Float, nullable=False)
    severity = Column(String, nullable=False) # e.g., 'critical', 'warning'
    is_enabled = Column(Boolean, default=True)

    asset = relationship("Asset", back_populates="alarm_rules")
