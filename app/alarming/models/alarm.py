# /app/alarming/models/alarm.py
"""
Modelo de la base de datos para la entidad Alarm.
"""
import uuid
from sqlalchemy import Column, String, Float, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.sql import func

class Alarm(Base):
    __tablename__ = "alarms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alarm_rule_id = Column(UUID(as_uuid=True), ForeignKey("alarm_rules.id"), nullable=False, index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    
    triggered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(TIMESTAMP(timezone=True))
    
    severity = Column(String)
    triggered_value = Column(Float)

    rule = relationship("AlarmRule")
    asset = relationship("Asset")
