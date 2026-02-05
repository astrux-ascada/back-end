# /app/procurement/api.py
"""
API Router para el módulo de Compras (Procurement).
"""
import logging
from typing import List
import uuid

from fastapi import APIRouter, Depends, status, HTTPException

from app.procurement import schemas
from app.procurement.service import ProcurementService
from app.dependencies.services import get_procurement_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.subscription import require_feature
from app.dependencies.permissions import require_permission

logger = logging.getLogger("app.procurement.api")

router = APIRouter(
    prefix="/procurement", 
    tags=["Procurement"],
    dependencies=[Depends(require_feature("module_procurement"))]
)

# --- Endpoints para Proveedores (Providers) ---

@router.post("/providers", response_model=schemas.ProviderRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("provider:create"))])
def create_provider(
    provider_in: schemas.ProviderCreate,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return procurement_service.create_provider(provider_in, tenant_id)

@router.get("/providers", response_model=List[schemas.ProviderRead], dependencies=[Depends(require_permission("provider:read"))])
def list_providers(
    skip: int = 0,
    limit: int = 100,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return procurement_service.list_providers(tenant_id, skip=skip, limit=limit)

@router.put("/providers/{provider_id}", response_model=schemas.ProviderRead, dependencies=[Depends(require_permission("provider:update"))])
def update_provider(
    provider_id: uuid.UUID,
    provider_in: schemas.ProviderUpdate,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return procurement_service.update_provider(provider_id, provider_in, tenant_id)

@router.delete("/providers/{provider_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permission("provider:delete"))])
def delete_provider(
    provider_id: uuid.UUID,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    procurement_service.delete_provider(provider_id, tenant_id)
    return None

# --- Endpoints para Repuestos (Spare Parts) ---

@router.post("/spare-parts", response_model=schemas.SparePartRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("spare_part:create"))])
def create_spare_part(
    spare_part_in: schemas.SparePartCreate,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return procurement_service.create_spare_part(spare_part_in, tenant_id)

@router.get("/spare-parts", response_model=List[schemas.SparePartRead], dependencies=[Depends(require_permission("spare_part:read"))])
def list_spare_parts(
    skip: int = 0,
    limit: int = 100,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return procurement_service.list_spare_parts(tenant_id, skip=skip, limit=limit)

@router.get("/spare-parts/{spare_part_id}", response_model=schemas.SparePartRead, dependencies=[Depends(require_permission("spare_part:read"))])
def get_spare_part(
    spare_part_id: uuid.UUID,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return procurement_service.get_spare_part(spare_part_id, tenant_id)

@router.put("/spare-parts/{spare_part_id}", response_model=schemas.SparePartRead, dependencies=[Depends(require_permission("spare_part:update"))])
def update_spare_part(
    spare_part_id: uuid.UUID,
    spare_part_in: schemas.SparePartUpdate,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return procurement_service.update_spare_part(spare_part_id, spare_part_in, tenant_id)

@router.delete("/spare-parts/{spare_part_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permission("spare_part:delete"))])
def delete_spare_part(
    spare_part_id: uuid.UUID,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    procurement_service.delete_spare_part(spare_part_id, tenant_id)
    return None
