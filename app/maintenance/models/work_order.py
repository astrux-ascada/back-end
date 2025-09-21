# /app/maintenance/models/work_order.py
"""
Modelo de la base de datos para la entidad WorkOrder.

Representa una orden de trabajo para realizar mantenimiento o una mejora
en un activo específico.
"""
import uuid

from sqlalchemy import Column, String, func, TIMESTAMP, ForeignKey, Text, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class WorkOrder(Base):
    """Modelo SQLAlchemy para una Orden de Trabajo."""
    __tablename__ = "work_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # --- Relación con el Activo ---
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    asset = relationship("Asset")

    # --- Campos de Inteligencia (Industria 5.0) ---
    category = Column(String(50), nullable=False, index=True, comment="CORRECTIVE, PREVENTIVE, PREDICTIVE, IMPROVEMENT")
    source_trigger = Column(JSONB, nullable=True, comment="JSON data explaining the origin of the work order.")

    # --- Campos de Estado y Prioridad ---
    status = Column(String(50), default="OPEN", nullable=False, index=True, comment="OPEN, IN_PROGRESS, ON_HOLD, COMPLETED, CANCELED")
    priority = Column(String(50), default="MEDIUM", nullable=False, index=True, comment="LOW, MEDIUM, HIGH, URGENT")

    # --- Campos Descriptivos ---
    summary = Column(String(255), nullable=False, comment="A brief, one-line summary of the work to be done.")
    description = Column(Text, nullable=True, comment="A detailed description of the issue and required work.")
    due_date = Column(Date, nullable=True)

    # --- Campos de Auditoría ---
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)
