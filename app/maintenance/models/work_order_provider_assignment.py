# /app/maintenance/models/work_order_provider_assignment.py
"""
Modelo de asociación para asignar Proveedores a Órdenes de Trabajo.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class WorkOrderProviderAssignment(Base):
    """Tabla de asociación para vincular WorkOrder y Provider."""
    __tablename__ = "work_order_provider_assignments"

    work_order_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.id"), primary_key=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), primary_key=True)

# Las relaciones inversas se definirán en app/maintenance/models/__init__.py
