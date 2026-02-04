# /app/core_engine/api.py
"""
API Router para el Core Engine.
"""
import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status

from app.core_engine import schemas
from app.core_engine.service import CoreEngineService
from app.dependencies.services import get_core_engine_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.permissions import require_permission
from app.identity.models import User
from app.dependencies.auth import get_current_active_user # Para obtener el usuario actual

logger = logging.getLogger("app.core_engine.api")

router = APIRouter(prefix="/data-sources", tags=["Core Engine - Data Sources"])

@router.post("/", response_model=schemas.DataSourceRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("data_source:create"))])
def create_data_source(
    ds_in: schemas.DataSourceCreate,
    core_engine_service: CoreEngineService = Depends(get_core_engine_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return core_engine_service.create_data_source(ds_in, tenant_id, current_user)

@router.get("/", response_model=List[schemas.DataSourceRead], dependencies=[Depends(require_permission("data_source:read"))])
def list_data_sources(
    skip: int = 0,
    limit: int = 100,
    core_engine_service: CoreEngineService = Depends(get_core_engine_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return core_engine_service.list_data_sources(tenant_id, skip, limit)

@router.get("/{ds_id}", response_model=schemas.DataSourceRead, dependencies=[Depends(require_permission("data_source:read"))])
def get_data_source(
    ds_id: uuid.UUID,
    core_engine_service: CoreEngineService = Depends(get_core_engine_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return core_engine_service.get_data_source(ds_id, tenant_id)

@router.put("/{ds_id}", response_model=schemas.DataSourceRead, dependencies=[Depends(require_permission("data_source:update"))])
def update_data_source(
    ds_id: uuid.UUID,
    ds_in: schemas.DataSourceUpdate,
    core_engine_service: CoreEngineService = Depends(get_core_engine_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return core_engine_service.update_data_source(ds_id, ds_in, tenant_id, current_user)

@router.delete("/{ds_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permission("data_source:delete"))])
def delete_data_source(
    ds_id: uuid.UUID,
    core_engine_service: CoreEngineService = Depends(get_core_engine_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    core_engine_service.delete_data_source(ds_id, tenant_id, current_user)
    return None
