# /app/configuration/api.py
"""
API Router para el módulo de Configuración del Sistema.

Define los endpoints para que un SuperUser gestione los parámetros y enums dinámicos.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, status

from app.configuration import schemas
from app.configuration.service import ConfigurationService
# --- MEJORA: Importar las dependencias correctas ---
from app.dependencies.services import get_configuration_service
from app.dependencies.auth import get_current_superuser

logger = logging.getLogger("app.configuration.api")

# Todos los endpoints en este módulo requieren privilegios de SuperUser.
router = APIRouter(
    prefix="/configuration", 
    tags=["Configuration"], 
    dependencies=[Depends(get_current_superuser)]
)


@router.get(
    "/parameters",
    summary="[SuperUser] Obtener todos los Parámetros de Configuración",
    response_model=List[schemas.ConfigurationParameterRead],
)
def list_parameters(config_service: ConfigurationService = Depends(get_configuration_service)):
    """Devuelve una lista de todos los parámetros de configuración del sistema."""
    return config_service.list_parameters()


@router.patch(
    "/parameters/{key}",
    summary="[SuperUser] Actualizar un Parámetro de Configuración",
    response_model=schemas.ConfigurationParameterRead,
)
def update_parameter(
    key: str,
    param_in: schemas.ConfigurationParameterUpdate,
    config_service: ConfigurationService = Depends(get_configuration_service),
):
    """Actualiza el valor de un parámetro de configuración específico."""
    return config_service.update_parameter(key, param_in)


@router.get(
    "/enums",
    summary="[SuperUser] Obtener todos los Enums Dinámicos",
    response_model=List[schemas.EnumTypeRead],
)
def list_enum_types(config_service: ConfigurationService = Depends(get_configuration_service)):
    """Devuelve una lista de todos los tipos de enums gestionables y sus valores."""
    return config_service.list_enum_types()


@router.post(
    "/enums/{enum_name}/values",
    summary="[SuperUser] Añadir un Valor a un Enum",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.EnumTypeRead,
)
def add_value_to_enum(
    enum_name: str,
    value_in: schemas.EnumValueCreate,
    config_service: ConfigurationService = Depends(get_configuration_service),
):
    """Añade un nuevo valor a un enum existente (ej: un nuevo estado para las órdenes de trabajo)."""
    return config_service.add_value_to_enum(enum_name, value_in)
