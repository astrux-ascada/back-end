# /app/auditing/models/approval_request.py
"""
Modelo para las Solicitudes de Aprobación (Maker-Checker).
"""
import uuid
import enum
from sqlalchemy import Column, String, ForeignKey, DateTime, func, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # --- Aislamiento ---
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

    # --- Actores ---
    requester_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    approver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # --- Contexto de la Acción ---
    entity_type = Column(String(50), nullable=False, index=True, comment="Ej: ASSET, WORK_ORDER")
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    action = Column(String(50), nullable=False, comment="Ej: DELETE, ARCHIVE")
    
    # Datos adicionales necesarios para ejecutar la acción (ej: payload de actualización)
    payload = Column(JSON, nullable=True)

    # --- Estado y Justificación ---
    status = Column(String(20), default=ApprovalStatus.PENDING, nullable=False, index=True)
    request_justification = Column(String(500), nullable=False)
    rejection_reason = Column(String(500), nullable=True)

    # --- Auditoría ---
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    responded_at = Column(DateTime(timezone=True), nullable=True)
