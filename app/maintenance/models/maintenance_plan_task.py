# /app/maintenance/models/maintenance_plan_task.py
import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class MaintenancePlanTask(Base):
    __tablename__ = "maintenance_plan_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("maintenance_plans.id"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    order = Column(Integer, nullable=False, default=0)

    plan = relationship("MaintenancePlan", back_populates="tasks")
