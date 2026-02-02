# /app/maintenance/models/maintenance_plan_task.py
"""
Modelo para las tareas predefinidas de un Plan de Mantenimiento.
"""
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class MaintenancePlanTask(Base):
    """
    Representa una tarea plantilla que se copiará a la Work Order
    cuando el plan se ejecute.
    """
    __tablename__ = "maintenance_plan_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    plan_id = Column(UUID(as_uuid=True), ForeignKey("maintenance_plans.id"), nullable=False, index=True)
    plan = relationship("MaintenancePlan", back_populates="tasks")
    
    description = Column(String(255), nullable=False)
    order = Column(Integer, default=1)
