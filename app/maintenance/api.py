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
from app.dependencies.auth import get_current_active_user
from app.dependencies.tenant import get_tenant_id # Importar dependencia de tenant
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

@router.post(
    "/work-orders",
    summary="Crear una nueva orden de trabajo",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.WorkOrderRead,
)
def create_work_order(
    work_order_in: schemas.WorkOrderCreate,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id), # Inyectar tenant
):
    """Crea una nueva orden de trabajo para el tenant actual."""
    try:
        return maintenance_service.create_work_order(work_order_in, current_user, tenant_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/work-orders/{work_order_id}",
    summary="Obtener detalles de una orden de trabajo",
    response_model=schemas.WorkOrderRead,
)
def get_work_order(
    work_order_id: uuid.UUID,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id), # Inyectar tenant
):
    """Obtiene la información de una orden de trabajo del tenant actual."""
    work_order = maintenance_service.get_work_order(work_order_id, tenant_id)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work Order not found")
    return work_order

@router.get(
    "/work-orders",
    summary="Listar órdenes de trabajo",
    response_model=List[schemas.WorkOrderRead],
)
def list_work_orders(
    skip: int = 0,
    limit: int = 100,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id), # Inyectar tenant
):
    """Lista las órdenes de trabajo del tenant actual."""
    return maintenance_service.list_work_orders(tenant_id, skip, limit)


@router.patch(
    "/work-orders/{work_order_id}/status",
    summary="Actualizar el estado de una orden de trabajo",
    response_model=schemas.WorkOrderRead,
)
def update_work_order_status(
    work_order_id: uuid.UUID,
    status_update: schemas.WorkOrderStatusUpdate,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id), # Inyectar tenant
):
    """Actualiza el estado de una orden de trabajo del tenant actual."""
    updated_work_order = maintenance_service.update_work_order_status(work_order_id, status_update, current_user, tenant_id)
    if not updated_work_order:
        raise HTTPException(status_code=404, detail="Work Order not found")
    return updated_work_order


@router.post(
    "/work-orders/assign-user",
    summary="Asignar un técnico a una orden de trabajo",
    status_code=status.HTTP_204_NO_CONTENT,
)
def assign_user_to_work_order(
    assignment_in: schemas.WorkOrderUserAssignmentCreate,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id), # Inyectar tenant
):
    """Asigna un usuario a una orden de trabajo, validando que ambos pertenezcan al tenant."""
    try:
        maintenance_service.assign_user_to_work_order(assignment_in, current_user, tenant_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
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
