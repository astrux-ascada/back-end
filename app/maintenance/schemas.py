# /app/maintenance/schemas.py
"""
Esquemas Pydantic para el módulo de Mantenimiento.
"""
import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.maintenance.models.work_order import WorkOrderStatus, WorkOrderPriority

# --- Esquemas para WorkOrder ---

class WorkOrderBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = None
    priority: WorkOrderPriority = WorkOrderPriority.MEDIUM
    asset_id: uuid.UUID
    scheduled_start_date: Optional[datetime] = None
    scheduled_end_date: Optional[datetime] = None

class WorkOrderCreate(WorkOrderBase):
    pass # Eliminado el campo 'tasks' que no estaba implementado

class WorkOrderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[WorkOrderPriority] = None
    status: Optional[WorkOrderStatus] = None
    scheduled_start_date: Optional[datetime] = None
    scheduled_end_date: Optional[datetime] = None

class WorkOrderCancel(BaseModel):
    cancellation_reason: str = Field(..., min_length=10, description="Motivo de la cancelación.")

class WorkOrderProviderAssignment(BaseModel):
    provider_id: uuid.UUID = Field(..., description="ID del proveedor externo a asignar.")
    notes: Optional[str] = Field(None, description="Notas adicionales para el proveedor.")
    estimated_cost: Optional[float] = Field(None, ge=0, description="Costo estimado del servicio externo.")

class WorkOrderRead(WorkOrderBase):
    id: uuid.UUID
    status: WorkOrderStatus
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    
    assigned_user_ids: List[uuid.UUID] = []
    assigned_provider_ids: List[uuid.UUID] = []

    class Config:
        from_attributes = True
