# /app/maintenance/models/work_order_user_assignment.py
"""
Modelo de asociación para asignar Usuarios a Órdenes de Trabajo.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class WorkOrderUserAssignment(Base):
    """Tabla de asociación para vincular WorkOrder y User."""
    __tablename__ = "work_order_user_assignments"

    work_order_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)

# Las relaciones inversas se definirán en app/maintenance/models/__init__.py
