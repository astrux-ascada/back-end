# /app/assets/api.py
"""
API Router para el módulo de Activos (Assets).
"""

import logging
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, status, HTTPException, Response, Body

from app.assets import schemas
from app.assets.service import AssetService
from app.dependencies.services import get_asset_service
from app.dependencies.auth import get_current_active_user
from app.dependencies.tenant import get_tenant_id
from app.dependencies.permissions import require_permission
from app.dependencies.limits import check_limit # Importar check_limit
from app.identity.models import User
from app.auditing.schemas import ApprovalRequestRead

logger = logging.getLogger("app.assets.api")

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/", response_model=List[schemas.AssetReadDTO], dependencies=[Depends(require_permission("asset:read"))])
def list_assets(
    type: Optional[str] = None,
    sectorId: Optional[uuid.UUID] = None,
    skip: int = 0,
    limit: int = 100,
    asset_service: AssetService = Depends(get_asset_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return asset_service.list_assets(tenant_id=tenant_id, skip=skip, limit=limit, category=type, sector_id=sectorId)

@router.get("/{asset_uuid}", response_model=schemas.AssetReadDTO, dependencies=[Depends(require_permission("asset:read"))])
def get_asset(
    asset_uuid: uuid.UUID,
    asset_service: AssetService = Depends(get_asset_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    asset = asset_service.get_asset(asset_id=asset_uuid, tenant_id=tenant_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset

@router.post(
    "/", 
    response_model=schemas.AssetReadDTO, 
    status_code=status.HTTP_201_CREATED, 
    dependencies=[
        Depends(require_permission("asset:create")),
        Depends(check_limit("assets")) # Aplicar el límite de activos
    ]
)
def create_asset(
    asset_in: schemas.AssetCreate,
    asset_service: AssetService = Depends(get_asset_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return asset_service.create_asset(asset_in=asset_in, user=current_user, tenant_id=tenant_id)

@router.put("/{asset_id}", response_model=schemas.AssetReadDTO, dependencies=[Depends(require_permission("asset:update"))])
def update_asset(
    asset_id: uuid.UUID,
    asset_in: schemas.AssetUpdate,
    asset_service: AssetService = Depends(get_asset_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    updated_asset = asset_service.update_asset(asset_id=asset_id, asset_in=asset_in, user=current_user, tenant_id=tenant_id)
    if not updated_asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return updated_asset

@router.patch("/{asset_uuid}/status", response_model=schemas.AssetReadDTO, dependencies=[Depends(require_permission("asset:update_status"))])
def update_asset_status(
    asset_uuid: uuid.UUID,
    status_update: schemas.AssetStatusUpdate,
    asset_service: AssetService = Depends(get_asset_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    updated_asset = asset_service.update_asset_status(asset_id=asset_uuid, status_update=status_update, user=current_user, tenant_id=tenant_id)
    if not updated_asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return updated_asset

@router.delete("/{asset_id}", response_model=ApprovalRequestRead, status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(require_permission("asset:delete"))])
def request_delete_asset(
    asset_id: uuid.UUID,
    justification: str = Body(..., embed=True, description="Justificación para solicitar el borrado del activo."),
    asset_service: AssetService = Depends(get_asset_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    try:
        approval_request = asset_service.request_delete_asset(asset_id, current_user, tenant_id, justification)
        return approval_request
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
