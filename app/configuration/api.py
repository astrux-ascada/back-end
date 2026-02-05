# /app/configuration/api.py
"""
API Router para el módulo de Configuración.
"""
from typing import List
import uuid

from fastapi import APIRouter, Depends, status, HTTPException

from app.configuration import schemas
from app.configuration.service import ConfigurationService
from app.dependencies.services import get_configuration_service
from app.dependencies.permissions import require_permission
from app.identity.models import User
from app.dependencies.auth import get_current_active_user # Para obtener el usuario actual

router = APIRouter(prefix="/configuration", tags=["Configuration"])

# --- Endpoints para ConfigurationParameter ---

@router.post("/parameters", response_model=schemas.ConfigurationParameterRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("config_param:create"))])
def create_parameter(
    param_in: schemas.ConfigurationParameterCreate,
    config_service: ConfigurationService = Depends(get_configuration_service),
    current_user: User = Depends(get_current_active_user)
):
    return config_service.create_parameter(param_in, current_user)

@router.get("/parameters", response_model=List[schemas.ConfigurationParameterRead], dependencies=[Depends(require_permission("config_param:read"))])
def list_parameters(
    config_service: ConfigurationService = Depends(get_configuration_service)
):
    return config_service.list_parameters()

@router.get("/parameters/{key}", response_model=schemas.ConfigurationParameterRead, dependencies=[Depends(require_permission("config_param:read"))])
def get_parameter(
    key: str,
    config_service: ConfigurationService = Depends(get_configuration_service)
):
    return config_service.get_parameter(key)

@router.put("/parameters/{key}", response_model=schemas.ConfigurationParameterRead, dependencies=[Depends(require_permission("config_param:update"))])
def update_parameter(
    key: str,
    param_in: schemas.ConfigurationParameterUpdate,
    config_service: ConfigurationService = Depends(get_configuration_service),
    current_user: User = Depends(get_current_active_user)
):
    return config_service.update_parameter(key, param_in, current_user)

@router.delete("/parameters/{key}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permission("config_param:delete"))])
def delete_parameter(
    key: str,
    config_service: ConfigurationService = Depends(get_configuration_service),
    current_user: User = Depends(get_current_active_user)
):
    config_service.delete_parameter(key, current_user)
    return None
