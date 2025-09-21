# /app/maintenance/api.py
"""
API Router para el módulo de Mantenimiento.

Define los endpoints para gestionar las órdenes de trabajo y sus asignaciones.
"""

import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status

from app.maintenance import schemas
from app.maintenance.service import MaintenanceService
# --- MEJORA: Importamos el inyector de dependencias desde la ubicación central ---
from app.dependencies.services import get_maintenance_service

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
):
    """Crea una nueva orden de trabajo para un activo."""
    return maintenance_service.create_work_order(work_order_in)

@router.get(
    "/work-orders/{work_order_id}",
    summary="Obtener detalles de una orden de trabajo",
    response_model=schemas.WorkOrderRead,
)
def get_work_order(
    work_order_id: uuid.UUID,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
):
    """Obtiene toda la información de una orden de trabajo, incluyendo sus tareas y asignaciones."""
    return maintenance_service.get_work_order(work_order_id)

@router.post(
    "/work-orders/assign-user",
    summary="Asignar un técnico a una orden de trabajo",
    status_code=status.HTTP_204_NO_CONTENT,
)
def assign_user_to_work_order(
    assignment_in: schemas.WorkOrderUserAssignmentCreate,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
):
    """Asigna un usuario (técnico) a una orden de trabajo existente."""
    maintenance_service.assign_user_to_work_order(assignment_in)
    return None # No content response

@router.post(
    "/work-orders/assign-provider",
    summary="Asignar un proveedor a una orden de trabajo",
    status_code=status.HTTP_204_NO_CONTENT,
)
def assign_provider_to_work_order(
    assignment_in: schemas.WorkOrderProviderAssignmentCreate,
    maintenance_service: MaintenanceService = Depends(get_maintenance_service),
):
    """Asigna un proveedor externo a una orden de trabajo existente."""
    maintenance_service.assign_provider_to_work_order(assignment_in)
    return None # No content response
