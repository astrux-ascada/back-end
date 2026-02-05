# /app/sectors/api.py
"""
API Router para el módulo de Sectores.
"""
import logging
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, status, HTTPException

from app.sectors import schemas
from app.sectors.service import SectorService
from app.dependencies.services import get_sector_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.permissions import require_permission
from app.dependencies.auth import get_current_active_user # Importar la dependencia
from app.identity.models import User

logger = logging.getLogger("app.sectors.api")

router = APIRouter(prefix="/sectors", tags=["Sectors"])

@router.post("/", response_model=schemas.SectorRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("sector:create"))])
def create_sector(
    sector_in: schemas.SectorCreate,
    sector_service: SectorService = Depends(get_sector_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return sector_service.create_sector(sector_in, tenant_id, current_user)

@router.get("/", response_model=List[schemas.SectorRead], dependencies=[Depends(require_permission("sector:read"))])
def list_sectors(
    parent_id: Optional[uuid.UUID] = None,
    skip: int = 0,
    limit: int = 100,
    sector_service: SectorService = Depends(get_sector_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return sector_service.list_sectors(tenant_id, skip=skip, limit=limit, parent_id=parent_id)

@router.get("/{sector_id}", response_model=schemas.SectorRead, dependencies=[Depends(require_permission("sector:read"))])
def get_sector(
    sector_id: uuid.UUID,
    sector_service: SectorService = Depends(get_sector_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return sector_service.get_sector(sector_id, tenant_id)

@router.put("/{sector_id}", response_model=schemas.SectorRead, dependencies=[Depends(require_permission("sector:update"))])
def update_sector(
    sector_id: uuid.UUID,
    sector_in: schemas.SectorUpdate,
    sector_service: SectorService = Depends(get_sector_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return sector_service.update_sector(sector_id, sector_in, tenant_id, current_user)

@router.delete("/{sector_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permission("sector:delete"))])
def delete_sector(
    sector_id: uuid.UUID,
    sector_service: SectorService = Depends(get_sector_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    sector_service.delete_sector(sector_id, tenant_id, current_user)
    return None
