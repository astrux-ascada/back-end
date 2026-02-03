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
from app.dependencies.subscription import require_feature # Importar la nueva dependencia

logger = logging.getLogger("app.procurement.api")

# Añadir la dependencia a nivel de router. Todas las rutas en este archivo
# requerirán que la feature 'module_procurement' esté activa.
router = APIRouter(
    prefix="/procurement", 
    tags=["Procurement"],
    dependencies=[Depends(require_feature("module_procurement"))]
)

# --- Endpoints para Proveedores (Providers) ---

@router.post(
    "/providers",
    summary="Crear un nuevo proveedor",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProviderRead,
)
def create_provider(
    provider_in: schemas.ProviderCreate,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    """Registra un nuevo proveedor para el tenant actual."""
    return procurement_service.create_provider(provider_in, tenant_id)


@router.get(
    "/providers",
    summary="Listar todos los proveedores",
    response_model=List[schemas.ProviderRead],
)
def list_providers(
    skip: int = 0,
    limit: int = 100,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    """Obtiene una lista paginada de todos los proveedores del tenant actual."""
    return procurement_service.list_providers(tenant_id, skip=skip, limit=limit)

# --- Endpoints para Repuestos (Spare Parts) ---

@router.post(
    "/spare-parts",
    summary="Crear un nuevo repuesto",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SparePartRead,
)
def create_spare_part(
    spare_part_in: schemas.SparePartCreate,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    """Registra un nuevo repuesto en el catálogo del tenant actual."""
    return procurement_service.create_spare_part(spare_part_in, tenant_id)


@router.get(
    "/spare-parts",
    summary="Listar todos los repuestos",
    response_model=List[schemas.SparePartRead],
)
def list_spare_parts(
    skip: int = 0,
    limit: int = 100,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    """Obtiene una lista paginada de todos los repuestos del tenant actual."""
    return procurement_service.list_spare_parts(tenant_id, skip=skip, limit=limit)

@router.get(
    "/spare-parts/{spare_part_id}",
    summary="Obtener un repuesto por su ID",
    response_model=schemas.SparePartRead,
)
def get_spare_part(
    spare_part_id: uuid.UUID,
    procurement_service: ProcurementService = Depends(get_procurement_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    """Obtiene los detalles de un repuesto específico del tenant actual."""
    spare_part = procurement_service.get_spare_part(spare_part_id, tenant_id)
    if not spare_part:
        raise HTTPException(status_code=404, detail="Spare Part not found")
    return spare_part
