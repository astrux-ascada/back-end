# /app/core_engine/api.py
"""
API Router para el módulo Core Engine.

Define los endpoints para gestionar las configuraciones de las fuentes de datos.
"""

import logging
from typing import List
import uuid

from fastapi import APIRouter, Depends, status

from app.core_engine import schemas
from app.core_engine.service import CoreEngineService
# --- MEJORA: Importamos el inyector de dependencias desde la ubicación central ---
from app.dependencies.services import get_core_engine_service

logger = logging.getLogger("app.core_engine.api")

router = APIRouter(prefix="/core-engine", tags=["Core Engine"])


@router.post(
    "/data-sources",
    summary="Crear una nueva fuente de datos",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DataSourceRead,
)
def create_data_source(
    data_source_in: schemas.DataSourceCreate,
    core_engine_service: CoreEngineService = Depends(get_core_engine_service),
):
    """Registra una nueva fuente de datos (ej: un PLC) en el sistema."""
    return core_engine_service.create_data_source(data_source_in)


@router.get(
    "/data-sources",
    summary="Listar todas las fuentes de datos",
    response_model=List[schemas.DataSourceRead],
)
def list_data_sources(
    skip: int = 0,
    limit: int = 100,
    core_engine_service: CoreEngineService = Depends(get_core_engine_service),
):
    """Obtiene una lista paginada de todas las fuentes de datos configuradas."""
    return core_engine_service.list_data_sources(skip=skip, limit=limit)
