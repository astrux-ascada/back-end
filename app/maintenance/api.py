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
# --- MEJORA: Importar dependencias de autenticación y el modelo de usuario ---
from app.dependencies.auth import get_current_active_user
from app.identity.models import User

logger = logging.getLogger("app.maintenance.api")

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


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
):
    """Crea una nueva orden de trabajo y registra la acción en la auditoría."""
    return maintenance_service.create_work_order(work_order_in, current_user)


@router.get(
    "/work-orders/{work_order_id}",
    summary="Obtener detalles de una orden de trabajo",
    response_model=schemas.WorkOrderRead,
)
def get_work_order(
    work_order_id: uuid.UUID,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
):
    """Obtiene toda la información de una orden de trabajo."""
    work_order = maintenance_service.get_work_order(work_order_id)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work Order not found")
    return work_order


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
):
    """Actualiza el estado de una orden de trabajo y registra la acción."""
    updated_work_order = maintenance_service.update_work_order_status(work_order_id, status_update, current_user)
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
):
    """Asigna un usuario a una orden de trabajo y registra la acción."""
    maintenance_service.assign_user_to_work_order(assignment_in, current_user)
    return None
