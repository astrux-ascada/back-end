# /app/maintenance/api.py
"""
API Router para el módulo de Mantenimiento.
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.maintenance import schemas
from app.maintenance.service import MaintenanceService
from app.maintenance.scheduler import MaintenanceScheduler
from app.dependencies.services import get_maintenance_service
from app.dependencies.auth import require_role
from app.identity.models import User
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

# --- Roles ---
VIEWER = "VIEWER"
TECHNICIAN = "TECHNICIAN"
MANAGER = "MAINTENANCE_MANAGER"

# --- Maintenance Plans Endpoints ---

@router.post("/plans", response_model=schemas.MaintenancePlanRead, status_code=201, dependencies=[Depends(require_role([MANAGER]))])
def create_maintenance_plan(plan_in: schemas.MaintenancePlanCreate, service: MaintenanceService = Depends(get_maintenance_service), current_user: User = Depends(require_role([MANAGER]))):
    return service.create_plan(plan_in, current_user)

@router.get("/plans", response_model=List[schemas.MaintenancePlanRead], dependencies=[Depends(require_role([VIEWER, TECHNICIAN, MANAGER]))])
def list_maintenance_plans(skip: int = 0, limit: int = 100, service: MaintenanceService = Depends(get_maintenance_service)):
    return service.list_plans(skip=skip, limit=limit)

@router.post("/plans/run-scheduler", status_code=200, dependencies=[Depends(require_role([MANAGER]))])
def trigger_scheduler(db: Session = Depends(get_db)):
    scheduler = MaintenanceScheduler(db)
    scheduler.run_preventive_maintenance_check()
    return {"message": "Scheduler execution finished."}

# --- Work Orders Endpoints ---

@router.post("/orders", response_model=schemas.WorkOrderRead, status_code=201, dependencies=[Depends(require_role([MANAGER]))])
def create_work_order(order_in: schemas.WorkOrderCreate, service: MaintenanceService = Depends(get_maintenance_service), current_user: User = Depends(require_role([MANAGER]))):
    return service.create_order(order_in, current_user)

@router.get("/orders", response_model=List[schemas.WorkOrderRead], dependencies=[Depends(require_role([VIEWER, TECHNICIAN, MANAGER]))])
def list_work_orders(skip: int = 0, limit: int = 100, status: Optional[str] = Query(None, description="Filtrar por estado"), asset_id: Optional[UUID] = Query(None, description="Filtrar por ID de activo"), service: MaintenanceService = Depends(get_maintenance_service)):
    return service.list_orders(skip=skip, limit=limit, status=status, asset_id=asset_id)

@router.get("/orders/{order_id}", response_model=schemas.WorkOrderRead, dependencies=[Depends(require_role([VIEWER, TECHNICIAN, MANAGER]))])
def get_work_order(order_id: UUID, service: MaintenanceService = Depends(get_maintenance_service)):
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")
    return order

@router.patch("/orders/{order_id}", response_model=schemas.WorkOrderRead, dependencies=[Depends(require_role([TECHNICIAN, MANAGER]))])
def update_work_order(order_id: UUID, order_in: schemas.WorkOrderUpdate, service: MaintenanceService = Depends(get_maintenance_service), current_user: User = Depends(require_role([TECHNICIAN, MANAGER]))):
    order = service.update_order(order_id, order_in, current_user)
    if not order:
        raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")
    return order

# --- Tasks Endpoints ---

@router.post("/orders/{order_id}/tasks", response_model=schemas.MaintenanceTaskRead, status_code=201, dependencies=[Depends(require_role([TECHNICIAN, MANAGER]))])
def add_task_to_order(order_id: UUID, task_in: schemas.MaintenanceTaskCreate, service: MaintenanceService = Depends(get_maintenance_service), current_user: User = Depends(require_role([TECHNICIAN, MANAGER]))):
    task = service.add_task_to_order(order_id, task_in, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")
    return task

@router.patch("/tasks/{task_id}", response_model=schemas.MaintenanceTaskRead, dependencies=[Depends(require_role([TECHNICIAN, MANAGER]))])
def update_task(task_id: UUID, task_in: schemas.MaintenanceTaskUpdate, service: MaintenanceService = Depends(get_maintenance_service), current_user: User = Depends(require_role([TECHNICIAN, MANAGER]))):
    task = service.update_task(task_id, task_in, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

# --- User Assignment Endpoints ---

@router.post("/orders/{order_id}/assign/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role([MANAGER]))])
def assign_user_to_order(order_id: UUID, user_id: UUID, service: MaintenanceService = Depends(get_maintenance_service), current_user: User = Depends(require_role([MANAGER]))):
    if not service.assign_user_to_order(order_id, user_id, current_user):
        raise HTTPException(status_code=404, detail="Orden de trabajo o usuario no encontrado")
    return None

@router.delete("/orders/{order_id}/assign/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role([MANAGER]))])
def unassign_user_from_order(order_id: UUID, user_id: UUID, service: MaintenanceService = Depends(get_maintenance_service), current_user: User = Depends(require_role([MANAGER]))):
    if not service.unassign_user_from_order(order_id, user_id, current_user):
        raise HTTPException(status_code=404, detail="Orden de trabajo o asignación no encontrada")
    return None

# --- Spare Part Assignment Endpoints ---

@router.post("/orders/{order_id}/spare-parts", response_model=schemas.WorkOrderRead, dependencies=[Depends(require_role([TECHNICIAN, MANAGER]))])
def add_spare_part_to_order(order_id: UUID, request: schemas.AddSparePartRequest, service: MaintenanceService = Depends(get_maintenance_service), current_user: User = Depends(require_role([TECHNICIAN, MANAGER]))):
    order = service.add_spare_part_to_order(order_id, request, current_user)
    if not order:
        raise HTTPException(status_code=404, detail="Orden de trabajo o repuesto no encontrado")
    return order

@router.delete("/orders/{order_id}/spare-parts/{part_id}", response_model=schemas.WorkOrderRead, dependencies=[Depends(require_role([TECHNICIAN, MANAGER]))])
def remove_spare_part_from_order(order_id: UUID, part_id: UUID, service: MaintenanceService = Depends(get_maintenance_service), current_user: User = Depends(require_role([TECHNICIAN, MANAGER]))):
    order = service.remove_spare_part_from_order(order_id, part_id, current_user)
    if not order:
        raise HTTPException(status_code=404, detail="Orden de trabajo o repuesto no encontrado")
    return order
