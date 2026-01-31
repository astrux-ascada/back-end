# /app/maintenance/schemas.py
"""
Esquemas Pydantic para el módulo de Mantenimiento.
"""
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, Field

# --- Enums / Constantes ---
PRIORITY_OPTIONS = ["LOW", "MEDIUM", "HIGH", "URGENT"]
STATUS_OPTIONS = ["OPEN", "IN_PROGRESS", "ON_HOLD", "COMPLETED", "CANCELED"]
CATEGORY_OPTIONS = ["CORRECTIVE", "PREVENTIVE", "PREDICTIVE", "IMPROVEMENT"]

# --- Esquemas para Planes de Mantenimiento ---

class MaintenancePlanTaskBase(BaseModel):
    description: str = Field(..., min_length=3, max_length=255)
    order: int = Field(1, ge=1)

class MaintenancePlanTaskCreate(MaintenancePlanTaskBase):
    pass

class MaintenancePlanTaskRead(MaintenancePlanTaskBase):
    id: UUID
    class Config:
        from_attributes = True

class MaintenancePlanBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100)
    description: Optional[str] = None
    asset_id: UUID
    summary_template: str = Field(..., min_length=5, max_length=255)
    category: str = "PREVENTIVE"
    priority: str = "MEDIUM"
    trigger_type: str = "TIME_BASED"
    interval_days: int = Field(..., gt=0)
    is_active: bool = True

class MaintenancePlanCreate(MaintenancePlanBase):
    tasks: List[MaintenancePlanTaskCreate] = []

class MaintenancePlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    summary_template: Optional[str] = None
    priority: Optional[str] = None
    interval_days: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None

class MaintenancePlanRead(MaintenancePlanBase):
    id: UUID
    last_execution_at: Optional[datetime] = None
    tasks: List[MaintenancePlanTaskRead] = []
    class Config:
        from_attributes = True


# --- Esquema de Repuestos (simplificado para la vista de mantenimiento) ---
class SparePartRequiredRead(BaseModel):
    id: UUID
    name: str
    part_number: Optional[str] = None
    
    class Config:
        from_attributes = True

class WorkOrderSparePartRead(BaseModel):
    spare_part: SparePartRequiredRead
    quantity_required: int

    class Config:
        from_attributes = True

class AddSparePartRequest(BaseModel):
    spare_part_id: UUID
    quantity_required: int = Field(1, gt=0)


# --- Esquemas de Tareas (Tasks) ---

class MaintenanceTaskBase(BaseModel):
    description: str = Field(..., min_length=3, max_length=255, description="Descripción de la tarea.")
    order: int = Field(1, description="Orden de ejecución.")

class MaintenanceTaskCreate(MaintenanceTaskBase):
    pass

class MaintenanceTaskUpdate(BaseModel):
    description: Optional[str] = None
    order: Optional[int] = None
    is_completed: Optional[bool] = None

class MaintenanceTaskRead(MaintenanceTaskBase):
    id: UUID
    work_order_id: UUID
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Esquemas de Usuarios Asignados (Simplificado) ---
class AssignedUserRead(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# --- Esquemas de Órdenes (Work Orders) ---

class WorkOrderBase(BaseModel):
    """Datos base compartidos para crear y leer órdenes."""
    summary: str = Field(..., min_length=5, max_length=255, description="Resumen breve del trabajo.")
    description: Optional[str] = Field(None, description="Descripción detallada.")
    priority: str = Field("MEDIUM", description="Prioridad: LOW, MEDIUM, HIGH, URGENT.")
    category: str = Field("CORRECTIVE", description="Categoría: CORRECTIVE, PREVENTIVE, etc.")
    due_date: Optional[date] = Field(None, description="Fecha límite.")
    asset_id: UUID = Field(..., description="ID del activo asociado.")
    source_trigger: Optional[Dict[str, Any]] = Field(None, description="Datos del origen (ej: alarma).")


class WorkOrderCreate(WorkOrderBase):
    """Datos necesarios para crear una nueva orden."""
    tasks: Optional[List[MaintenanceTaskCreate]] = None
    assigned_user_ids: Optional[List[UUID]] = None


class WorkOrderUpdate(BaseModel):
    """Datos para actualizar una orden existente."""
    summary: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    source_trigger: Optional[Dict[str, Any]] = None


class WorkOrderRead(WorkOrderBase):
    """Esquema de respuesta con datos del sistema."""
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    tasks: List[MaintenanceTaskRead] = []
    assigned_users: List[AssignedUserRead] = []
    required_spare_parts: List[WorkOrderSparePartRead] = []

    class Config:
        from_attributes = True
