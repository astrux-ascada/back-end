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
from app.dependencies.auth import require_role
from app.core.exceptions import NotFoundException

logger = logging.getLogger("app.procurement.api")

router = APIRouter(prefix="/procurement", tags=["Procurement"])

# --- Roles ---
VIEWER = "VIEWER"
TECHNICIAN = "TECHNICIAN"
MANAGER = "MAINTENANCE_MANAGER"

# --- Provider Endpoints ---

@router.post("/providers", summary="Crear un nuevo proveedor", status_code=status.HTTP_201_CREATED, response_model=schemas.ProviderRead, dependencies=[Depends(require_role([MANAGER]))])
def create_provider(provider_in: schemas.ProviderCreate, service: ProcurementService = Depends(get_procurement_service)):
    return service.create_provider(provider_in)

@router.get("/providers", summary="Listar proveedores activos", response_model=List[schemas.ProviderRead], dependencies=[Depends(require_role([VIEWER, TECHNICIAN, MANAGER]))])
def list_providers(skip: int = 0, limit: int = 100, service: ProcurementService = Depends(get_procurement_service)):
    return service.list_providers(skip=skip, limit=limit)

@router.get("/providers/{provider_id}", summary="Obtener un proveedor", response_model=schemas.ProviderRead, dependencies=[Depends(require_role([VIEWER, TECHNICIAN, MANAGER]))])
def get_provider(provider_id: uuid.UUID, service: ProcurementService = Depends(get_procurement_service)):
    provider = service.get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado.")
    return provider

@router.put("/providers/{provider_id}", summary="Actualizar un proveedor", response_model=schemas.ProviderRead, dependencies=[Depends(require_role([MANAGER]))])
def update_provider(provider_id: uuid.UUID, provider_in: schemas.ProviderUpdate, service: ProcurementService = Depends(get_procurement_service)):
    try:
        return service.update_provider(provider_id, provider_in)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/providers/{provider_id}", summary="Desactivar un proveedor", response_model=schemas.ProviderRead, dependencies=[Depends(require_role([MANAGER]))])
def delete_provider(provider_id: uuid.UUID, service: ProcurementService = Depends(get_procurement_service)):
    try:
        return service.soft_delete_provider(provider_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# --- Spare Part Endpoints ---

@router.post("/spare-parts", summary="Crear un nuevo repuesto", status_code=status.HTTP_201_CREATED, response_model=schemas.SparePartRead, dependencies=[Depends(require_role([MANAGER]))])
def create_spare_part(part_in: schemas.SparePartCreate, service: ProcurementService = Depends(get_procurement_service)):
    return service.create_spare_part(part_in)

@router.get("/spare-parts", summary="Listar repuestos activos", response_model=List[schemas.SparePartRead], dependencies=[Depends(require_role([VIEWER, TECHNICIAN, MANAGER]))])
def list_spare_parts(skip: int = 0, limit: int = 100, service: ProcurementService = Depends(get_procurement_service)):
    return service.list_spare_parts(skip=skip, limit=limit)

@router.get("/spare-parts/{part_id}", summary="Obtener un repuesto", response_model=schemas.SparePartRead, dependencies=[Depends(require_role([VIEWER, TECHNICIAN, MANAGER]))])
def get_spare_part(part_id: uuid.UUID, service: ProcurementService = Depends(get_procurement_service)):
    part = service.get_spare_part(part_id)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repuesto no encontrado.")
    return part

@router.put("/spare-parts/{part_id}", summary="Actualizar un repuesto", response_model=schemas.SparePartRead, dependencies=[Depends(require_role([MANAGER]))])
def update_spare_part(part_id: uuid.UUID, part_in: schemas.SparePartUpdate, service: ProcurementService = Depends(get_procurement_service)):
    try:
        return service.update_spare_part(part_id, part_in)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
