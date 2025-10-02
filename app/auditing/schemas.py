# /app/auditing/schemas.py
"""
Esquemas Pydantic para el módulo de Auditoría.
"""
import uuid
from datetime import datetime
from typing import Optional, Any, Dict

from pydantic import BaseModel, Field


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
