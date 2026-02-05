# /app/maintenance/models/maintenance_plan.py
import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, Interval, DateTime, Boolean, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class MaintenancePlan(Base):
    __tablename__ = "maintenance_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    summary_template = Column(String, nullable=True)
    category = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    trigger_type = Column(String, nullable=False) # e.g., "TIME_BASED", "METER_BASED"
    interval_days = Column(Integer, nullable=True) # For time-based
    last_execution_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    asset = relationship("Asset") # back_populates a definir en Asset
    tasks = relationship("MaintenancePlanTask", back_populates="plan")
