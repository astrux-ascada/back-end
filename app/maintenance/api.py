# /app/maintenance/api.py
"""
API Router para el módulo de Mantenimiento.
"""
import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from app.maintenance import schemas
from app.maintenance.service import MaintenanceService
from app.dependencies.services import get_maintenance_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.auth import get_current_active_user
from app.dependencies.permissions import require_permission
from app.identity.models import User

logger = logging.getLogger("app.maintenance.api")

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

@router.post("/work-orders", response_model=schemas.WorkOrderRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("work_order:create"))])
def create_work_order(
    work_order_in: schemas.WorkOrderCreate,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return maintenance_service.create_work_order(work_order_in, tenant_id, current_user)

@router.get("/work-orders", response_model=List[schemas.WorkOrderRead], dependencies=[Depends(require_permission("work_order:read"))])
def list_work_orders(
    skip: int = 0,
    limit: int = 100,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return maintenance_service.list_work_orders(tenant_id, skip, limit)

@router.get("/work-orders/{work_order_id}", response_model=schemas.WorkOrderRead, dependencies=[Depends(require_permission("work_order:read"))])
def get_work_order(
    work_order_id: uuid.UUID,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return maintenance_service.get_work_order(work_order_id, tenant_id)

@router.put("/work-orders/{work_order_id}", response_model=schemas.WorkOrderRead, dependencies=[Depends(require_permission("work_order:update"))])
def update_work_order(
    work_order_id: uuid.UUID,
    work_order_in: schemas.WorkOrderUpdate,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return maintenance_service.update_work_order(work_order_id, work_order_in, tenant_id, current_user)

@router.patch("/work-orders/{work_order_id}/cancel", response_model=schemas.WorkOrderRead, dependencies=[Depends(require_permission("work_order:cancel"))])
def cancel_work_order(
    work_order_id: uuid.UUID,
    cancel_in: schemas.WorkOrderCancel,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return maintenance_service.cancel_work_order(work_order_id, cancel_in, tenant_id, current_user)

@router.post("/work-orders/{work_order_id}/assign-provider", response_model=schemas.WorkOrderRead, dependencies=[Depends(require_permission("work_order:assign_provider"))])
def assign_provider_to_work_order(
    work_order_id: uuid.UUID,
    assignment_in: schemas.WorkOrderProviderAssignment,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return maintenance_service.assign_provider(work_order_id, assignment_in, tenant_id, current_user)
