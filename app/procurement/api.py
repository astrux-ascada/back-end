# /app/procurement/api.py
"""
API Router para el módulo de Compras (Procurement).

Define los endpoints para gestionar proveedores.
"""

import logging
from typing import List
import uuid

from fastapi import APIRouter, Depends, status, HTTPException

from app.procurement import schemas
from app.procurement.service import ProcurementService
from app.dependencies.services import get_procurement_service
# --- MODIFICADO: Importar dependencias de autenticación ---
from app.dependencies.auth import get_current_admin_user, get_current_active_user
from app.core.exceptions import NotFoundException

logger = logging.getLogger("app.procurement.api")

router = APIRouter(prefix="/procurement", tags=["Procurement"])


@router.post(
    "/providers",
    summary="Crear un nuevo proveedor",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProviderRead,
    dependencies=[Depends(get_current_admin_user)]
)
def create_provider(
    provider_in: schemas.ProviderCreate,
    procurement_service: ProcurementService = Depends(get_procurement_service),
):
    """Registra un nuevo proveedor en el sistema. Solo para Admins y Super Users."""
    return procurement_service.create_provider(provider_in)


@router.get(
    "/providers",
    summary="Listar todos los proveedores activos",
    response_model=List[schemas.ProviderRead],
    dependencies=[Depends(get_current_active_user)]
)
def list_providers(
    skip: int = 0,
    limit: int = 100,
    procurement_service: ProcurementService = Depends(get_procurement_service),
):
    """Obtiene una lista paginada de todos los proveedores activos."""
    return procurement_service.list_providers(skip=skip, limit=limit)


@router.get(
    "/providers/{provider_id}",
    summary="Obtener un proveedor por su ID",
    response_model=schemas.ProviderRead,
    dependencies=[Depends(get_current_active_user)]
)
def get_provider(
    provider_id: uuid.UUID,
    procurement_service: ProcurementService = Depends(get_procurement_service),
):
    """Obtiene los detalles de un proveedor específico, esté activo o no."""
    provider = procurement_service.get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado.")
    return provider


@router.put(
    "/providers/{provider_id}",
    summary="Actualizar un proveedor",
    response_model=schemas.ProviderRead,
    dependencies=[Depends(get_current_admin_user)]
)
def update_provider(
    provider_id: uuid.UUID,
    provider_in: schemas.ProviderUpdate,
    procurement_service: ProcurementService = Depends(get_procurement_service),
):
    """Actualiza la información de un proveedor. Permite reactivar un proveedor con `is_active: true`."""
    try:
        return procurement_service.update_provider(provider_id, provider_in)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/providers/{provider_id}",
    summary="Desactivar un proveedor (Soft Delete)",
    response_model=schemas.ProviderRead, # <-- MODIFICADO: Devuelve el proveedor desactivado
    dependencies=[Depends(get_current_admin_user)]
)
def delete_provider(
    provider_id: uuid.UUID,
    procurement_service: ProcurementService = Depends(get_procurement_service),
):
    """Desactiva un proveedor en el sistema (borrado lógico). Solo para Admins y Super Users."""
    try:
        # --- MODIFICADO: Llama al método de soft delete ---
        deleted_provider = procurement_service.soft_delete_provider(provider_id)
        return deleted_provider
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
