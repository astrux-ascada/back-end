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
# --- MODIFICADO: Importar dependencias de autenticación y el modelo de usuario ---
from app.dependencies.auth import get_current_active_user, get_current_admin_user
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
):
    """Devuelve una lista de todos los activos, con soporte para filtros."""
    return asset_service.list_assets(skip=skip, limit=limit, category=type, sector_id=sectorId)


@router.get(
    "/{uuid}",
    summary="Obtener un Activo por su UUID",
    response_model=schemas.AssetReadDTO,
)
def get_asset(
    uuid: uuid.UUID,
    asset_service: AssetService = Depends(get_asset_service),
):
    """Devuelve los detalles de un activo específico."""
    asset = asset_service.get_asset(uuid)
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
):
    """Registra un nuevo activo físico en la planta y registra la acción."""
    return asset_service.create_asset(asset_in, current_user)


@router.put(
    "/{asset_id}",
    summary="Actualizar un activo existente",
    response_model=schemas.AssetReadDTO,
    dependencies=[Depends(get_current_admin_user)] # <-- AÑADIDO: Endpoint protegido
)
def update_asset(
    asset_id: uuid.UUID,
    asset_in: schemas.AssetUpdate,
    asset_service: AssetService = Depends(get_asset_service),
    current_user: User = Depends(get_current_admin_user),
):
    """Actualiza los detalles de un activo existente. Solo para Admins y Super Users."""
    updated_asset = asset_service.update_asset(asset_id, asset_in, current_user)
    if not updated_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return updated_asset


@router.patch(
    "/{uuid}/status",
    summary="Actualizar el Estado de un Activo",
    response_model=schemas.AssetReadDTO,
)
def update_asset_status(
    uuid: uuid.UUID,
    status_update: schemas.AssetStatusUpdate,
    asset_service: AssetService = Depends(get_asset_service),
    current_user: User = Depends(get_current_active_user),
):
    """Actualiza el estado operativo de un activo específico y registra la acción."""
    updated_asset = asset_service.update_asset_status(uuid, status_update, current_user)
    if not updated_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return updated_asset
