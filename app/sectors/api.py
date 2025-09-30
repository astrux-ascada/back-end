# /app/sectors/api.py
"""
API Router para el módulo de Sectores.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, status

from app.sectors import schemas
from app.sectors.service import SectorService
# --- MEJORA: Importamos el inyector de dependencias desde la ubicación central ---
from app.dependencies.services import get_sector_service

logger = logging.getLogger("app.sectors.api")

router = APIRouter(prefix="/sectors", tags=["Sectors"])


@router.post(
    "/",
    summary="Crear un nuevo sector",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SectorRead,
)
def create_sector(
    sector_in: schemas.SectorCreate,
    sector_service: SectorService = Depends(get_sector_service),
):
    """Crea un nuevo sector en la planta."""
    return sector_service.create_sector(sector_in)


@router.get(
    "/",
    summary="Listar todos los sectores",
    response_model=List[schemas.SectorRead],
)
def list_sectors(
    skip: int = 0,
    limit: int = 100,
    sector_service: SectorService = Depends(get_sector_service),
):
    """Obtiene una lista paginada de todos los sectores."""
    return sector_service.list_sectors(skip=skip, limit=limit)
