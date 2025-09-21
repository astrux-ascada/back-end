# /app/maintenance/models/work_order_user_assignment.py
"""
Modelo de asociación para asignar Usuarios a Órdenes de Trabajo.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.maintenance.models.work_order import WorkOrder
from app.identity.models.user import User


class WorkOrderUserAssignment(Base):
    """Tabla de asociación para vincular WorkOrder y User."""
    __tablename__ = "work_order_user_assignments"

    work_order_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)

# Añadir las relaciones inversas a los modelos principales
WorkOrder.assigned_users = relationship("User", secondary="work_order_user_assignments", back_populates="work_orders")
User.work_orders = relationship("WorkOrder", secondary="work_order_user_assignments", back_populates="assigned_users")
