# /app/maintenance/schemas.py
"""
Esquemas Pydantic para el módulo de Mantenimiento.

Define los contratos de datos para la API, cubriendo WorkOrder, MaintenanceTask
y las asignaciones de personal y proveedores.
"""
import uuid
from datetime import date, datetime
from typing import Optional, List, Any

from pydantic import BaseModel, Field, Json

# --- MEJORA: Importar el DTO correcto de Assets para anidarlo ---
from app.assets.schemas import AssetReadDTO
from app.identity.schemas import UserRead
from app.procurement.schemas import ProviderRead


# --- Esquemas para MaintenanceTask ---

class MaintenanceTaskBase(BaseModel):
    description: str = Field(..., example="Reemplazar filtro de aceite principal.")
    order: int = Field(1, gt=0, example=1)

class MaintenanceTaskCreate(MaintenanceTaskBase):
    work_order_id: uuid.UUID

class MaintenanceTaskRead(MaintenanceTaskBase):
    id: uuid.UUID
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --- Esquemas para WorkOrder ---

class WorkOrderBase(BaseModel):
    asset_id: uuid.UUID = Field(..., description="ID del activo que requiere mantenimiento.")
    category: str = Field(..., example="PREDICTIVE", description="CORRECTIVE, PREVENTIVE, PREDICTIVE, IMPROVEMENT")
    status: str = Field("OPEN", example="OPEN")
    priority: str = Field("MEDIUM", example="MEDIUM")
    summary: str = Field(..., example="Fallo inminente detectado en el motor principal.")
    description: Optional[str] = Field(None, example="El análisis de vibraciones indica un desgaste del 85% en el rodamiento A-3.")
    due_date: Optional[date] = None
    source_trigger: Optional[Json[Any]] = Field(None, description="JSON data explaining the origin of the work order.")

class WorkOrderCreate(WorkOrderBase):
    pass

class WorkOrderRead(WorkOrderBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    # --- MEJORA: La relación anidada ahora usa el DTO correcto de Asset ---
    asset: AssetReadDTO
    tasks: List[MaintenanceTaskRead] = []
    assigned_users: List[UserRead] = []
    assigned_provider: Optional[ProviderRead] = None

    class Config:
        from_attributes = True


# --- Esquemas para Asignaciones ---

class WorkOrderUserAssignmentCreate(BaseModel):
    work_order_id: uuid.UUID
    user_id: uuid.UUID

class WorkOrderProviderAssignmentCreate(BaseModel):
    work_order_id: uuid.UUID
    provider_id: uuid.UUID
