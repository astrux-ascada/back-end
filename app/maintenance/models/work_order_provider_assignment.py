# /app/maintenance/models/work_order_provider_assignment.py
"""
Modelo de asociación para asignar Proveedores a Órdenes de Trabajo.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.maintenance.models.work_order import WorkOrder
from app.procurement.models.provider import Provider


class WorkOrderProviderAssignment(Base):
    """Tabla de asociación para vincular WorkOrder y Provider."""
    __tablename__ = "work_order_provider_assignments"

    work_order_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.id"), primary_key=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), primary_key=True)

# Añadir las relaciones inversas a los modelos principales
WorkOrder.assigned_provider = relationship("Provider", secondary="work_order_provider_assignments", back_populates="work_orders")
Provider.work_orders = relationship("WorkOrder", secondary="work_order_provider_assignments", back_populates="assigned_provider")
