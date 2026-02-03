# /app/assets/api.py
"""
API Router para el módulo de Activos (Assets), alineado con el contrato de API.
"""

import logging
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, status, HTTPException

from app.assets import schemas
from app.assets.service import AssetService
from app.dependencies.services import get_asset_service
from app.dependencies.auth import get_current_active_user
from app.dependencies.tenant import get_tenant_id # Importar la nueva dependencia
from app.identity.models import User

logger = logging.getLogger("app.assets.api")

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get(
    "/",
    summary="Obtener todos los Activos con filtros",
    response_model=List[schemas.AssetReadDTO],
)
def list_assets(
    type: Optional[str] = None,
    sectorId: Optional[uuid.UUID] = None,
    skip: int = 0,
    limit: int = 100,
    asset_service: AssetService = Depends(get_asset_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id), # Inyectar tenant_id
):
    """Devuelve una lista de todos los activos del tenant actual."""
    return asset_service.list_assets(
        tenant_id=tenant_id, skip=skip, limit=limit, category=type, sector_id=sectorId
    )


@router.get(
    "/{asset_uuid}",
    summary="Obtener un Activo por su UUID",
    response_model=schemas.AssetReadDTO,
)
def get_asset(
    asset_uuid: uuid.UUID,
    asset_service: AssetService = Depends(get_asset_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id), # Inyectar tenant_id
):
    """Devuelve los detalles de un activo específico del tenant actual."""
    asset = asset_service.get_asset(asset_id=asset_uuid, tenant_id=tenant_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.post(
    "/",
    summary="Crear una nueva instancia de activo físico",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AssetReadDTO,
)
def create_asset(
    asset_in: schemas.AssetCreate,
    asset_service: AssetService = Depends(get_asset_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id), # Inyectar tenant_id
):
    """Registra un nuevo activo físico en el tenant actual."""
    return asset_service.create_asset(asset_in=asset_in, user=current_user, tenant_id=tenant_id)


@router.put(
    "/{asset_id}",
    summary="Actualizar un activo existente",
    response_model=schemas.AssetReadDTO,
)
def update_asset(
    asset_id: uuid.UUID,
    asset_in: schemas.AssetUpdate,
    asset_service: AssetService = Depends(get_asset_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id), # Inyectar tenant_id
):
    """Actualiza los detalles de un activo existente en el tenant actual."""
    updated_asset = asset_service.update_asset(
        asset_id=asset_id, asset_in=asset_in, user=current_user, tenant_id=tenant_id
    )
    if not updated_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return updated_asset


@router.patch(
    "/{asset_uuid}/status",
    summary="Actualizar el Estado de un Activo",
    response_model=schemas.AssetReadDTO,
)
def update_asset_status(
    asset_uuid: uuid.UUID,
    status_update: schemas.AssetStatusUpdate,
    asset_service: AssetService = Depends(get_asset_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id), # Inyectar tenant_id
):
    """Actualiza el estado operativo de un activo específico en el tenant actual."""
    updated_asset = asset_service.update_asset_status(
        asset_id=asset_uuid, status_update=status_update, user=current_user, tenant_id=tenant_id
    )
    if not updated_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return updated_asset
