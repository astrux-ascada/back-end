# /app/auditing/schemas.py
"""
Esquemas Pydantic para el módulo de Auditoría y Aprobaciones.
"""
import uuid
from datetime import datetime
from typing import Optional, Any, Dict

from pydantic import BaseModel, Field
from app.auditing.models.approval_request import ApprovalStatus


# --- Audit Log ---

class AuditLogBase(BaseModel):
    user_id: Optional[uuid.UUID] = Field(None, description="ID del usuario que realizó la acción.")
    entity_type: str = Field(..., example="WorkOrder", description="Tipo de la entidad modificada.")
    entity_id: uuid.UUID = Field(..., description="ID de la entidad modificada.")
    action: str = Field(..., example="UPDATE_STATUS", description="La acción realizada.")
    details: Optional[Dict[str, Any]] = Field(None, description="JSON con los detalles del cambio.")


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogRead(AuditLogBase):
    id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True

# --- Approval Request ---

class ApprovalRequestBase(BaseModel):
    entity_type: str = Field(..., example="ASSET", description="Tipo de recurso a modificar.")
    entity_id: uuid.UUID = Field(..., description="ID del recurso.")
    action: str = Field(..., example="DELETE", description="Acción solicitada.")
    payload: Optional[Dict[str, Any]] = Field(None, description="Datos necesarios para ejecutar la acción.")
    request_justification: str = Field(..., min_length=10, description="Motivo de la solicitud.")

class ApprovalRequestCreate(ApprovalRequestBase):
    pass

class ApprovalRequestRead(ApprovalRequestBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    requester_id: uuid.UUID
    approver_id: Optional[uuid.UUID]
    status: ApprovalStatus
    rejection_reason: Optional[str]
    created_at: datetime
    updated_at: datetime
    responded_at: Optional[datetime]

    class Config:
        from_attributes = True

class ApprovalDecision(BaseModel):
    approved: bool = Field(..., description="True para aprobar, False para rechazar.")
    rejection_reason: Optional[str] = Field(None, description="Obligatorio si se rechaza.")
