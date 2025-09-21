# /app/procurement/api.py
"""
API Router para el módulo de Compras (Procurement).

Define los endpoints para gestionar proveedores.
"""

import logging
from typing import List
import uuid

from fastapi import APIRouter, Depends, status

from app.procurement import schemas
from app.procurement.service import ProcurementService
# --- MEJORA: Importamos el inyector de dependencias desde la ubicación central ---
from app.dependencies.services import get_procurement_service

logger = logging.getLogger("app.procurement.api")

router = APIRouter(prefix="/procurement", tags=["Procurement"])


@router.post(
    "/providers",
    summary="Crear un nuevo proveedor",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProviderRead,
)
def create_provider(
    provider_in: schemas.ProviderCreate,
    procurement_service: ProcurementService = Depends(get_procurement_service),
):
    """Registra un nuevo proveedor en el sistema."""
    return procurement_service.create_provider(provider_in)


@router.get(
    "/providers",
    summary="Listar todos los proveedores",
    response_model=List[schemas.ProviderRead],
)
def list_providers(
    skip: int = 0,
    limit: int = 100,
    procurement_service: ProcurementService = Depends(get_procurement_service),
):
    """Obtiene una lista paginada de todos los proveedores."""
    return procurement_service.list_providers(skip=skip, limit=limit)
