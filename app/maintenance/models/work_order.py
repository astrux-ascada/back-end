# /app/maintenance/models/work_order.py
"""
Modelo de la base de datos para la entidad WorkOrder.
"""
import uuid
import enum
from sqlalchemy import Column, String, func, TIMESTAMP, ForeignKey, Text, Date, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# --- Enums para Estado y Prioridad ---

class WorkOrderStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class WorkOrderPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class WorkOrder(Base):
    """Modelo SQLAlchemy para una Orden de Trabajo."""
    __tablename__ = "work_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    asset = relationship("Asset")

    category = Column(String(50), nullable=False, index=True, comment="CORRECTIVE, PREVENTIVE, PREDICTIVE, IMPROVEMENT")
    source_trigger = Column(JSONB, nullable=True)

    # Usamos String en la BD pero validamos con Enum en la aplicación
    status = Column(String(50), default=WorkOrderStatus.OPEN, nullable=False, index=True)
    priority = Column(String(50), default=WorkOrderPriority.MEDIUM, nullable=False, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)
    
    cancellation_reason = Column(Text, nullable=True)

    # --- Campos de Evaluación (IA Feedback Loop) ---
    rating = Column(Integer, nullable=True, comment="Calificación de la ejecución (1-5).")
    feedback = Column(Text, nullable=True, comment="Comentarios cualitativos sobre la ejecución.")

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)
