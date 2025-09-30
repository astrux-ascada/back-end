# /app/maintenance/models/maintenance_task.py
"""
Modelo de la base de datos para la entidad MaintenanceTask.

Representa una tarea o paso específico dentro de una WorkOrder.
"""
import uuid

from sqlalchemy import Column, String, func, TIMESTAMP, ForeignKey, Integer, Boolean, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class MaintenanceTask(Base):
    """Modelo SQLAlchemy para una Tarea de Mantenimiento (Checklist)."""
    __tablename__ = "maintenance_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # --- Relación con la Orden de Trabajo ---
    work_order_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.id"), nullable=False,
                           index=True)
    work_order = relationship("WorkOrder", back_populates="tasks")

    # --- Campos de la Tarea ---
    description = Column(String(255), nullable=False,
                         comment="Description of the specific task to be performed.")
    order = Column(Integer, default=1,
                   comment="The sequence order of the task within the work order.")
    is_completed = Column(Boolean, default=False, nullable=False)

    # --- Campos de Auditoría ---
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(),
                        nullable=False)

 
# La relación inversa se define en app/maintenance/models/__init__.py para evitar dependencias circulares.
 
