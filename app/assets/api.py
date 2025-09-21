# /app/assets/api.py
"""
API Router para el módulo de Activos (Assets).

Define los endpoints para gestionar el catálogo de tipos de activos, las instancias
de activos físicos y sus jerarquías.
"""

import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status

from app.assets import schemas
from app.assets.service import AssetService
# --- MEJORA: Importamos el inyector de dependencias desde la ubicación central ---
from app.dependencies.services import get_asset_service

logger = logging.getLogger("app.assets.api")

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.post(
    "/types",
    summary="Crear un nuevo tipo de activo",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AssetTypeRead,
)
def create_asset_type(
    asset_type_in: schemas.AssetTypeCreate,
    asset_service: AssetService = Depends(get_asset_service),
):
    """Crea una nueva plantilla de activo en el catálogo."""
    return asset_service.create_asset_type(asset_type_in)


@router.post(
    "/",
    summary="Crear una nueva instancia de activo físico",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AssetRead,
)
def create_asset(
    asset_in: schemas.AssetCreate,
    asset_service: AssetService = Depends(get_asset_service),
):
    """Registra un nuevo activo físico en la planta."""
    return asset_service.create_asset(asset_in)


@router.post(
    "/hierarchy",
    summary="Añadir un componente a la jerarquía de un tipo de activo",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AssetHierarchyRead,
)
def add_component_to_hierarchy(
    hierarchy_in: schemas.AssetHierarchyCreate,
    asset_service: AssetService = Depends(get_asset_service),
):
    """Define una relación padre-hijo entre dos tipos de activo."""
    return asset_service.add_component(hierarchy_in)
