# /app/maintenance/models/work_order_spare_part.py
"""
Modelo de asociación para vincular Repuestos (Spare Parts) a Órdenes de Trabajo.
"""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class WorkOrderSparePart(Base):
    """
    Tabla de asociación que define qué repuestos y en qué cantidad
    se requieren para una Orden de Trabajo.
    """
    __tablename__ = "work_order_spare_parts"

    work_order_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.id"), primary_key=True)
    spare_part_id = Column(UUID(as_uuid=True), ForeignKey("spare_parts.id"), primary_key=True)
    
    quantity_required = Column(Integer, nullable=False, default=1, comment="Cantidad del repuesto necesaria para la orden.")
