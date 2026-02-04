# /app/alarming/api.py
"""
API Router para el módulo de Alertas (Alarming).
"""
import logging
from typing import List
import uuid

from fastapi import APIRouter, Depends, status, HTTPException

from app.alarming.schemas import AlarmRead
from app.alarming.service import AlarmingService
from app.dependencies.services import get_alarming_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.auth import get_current_active_user
from app.dependencies.permissions import require_permission
from app.identity.models import User

logger = logging.getLogger("app.alarming.api")

router = APIRouter(prefix="/alarming", tags=["Alarming"])

# --- Endpoints para Reglas de Alarma (Alarm Rules) ---

@router.post("/rules", response_model=schemas.AlarmRule, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("alarm_rule:create"))])
def create_alarm_rule(
    rule_in: schemas.AlarmRuleCreate,
    alarming_service: AlarmingService = Depends(get_alarming_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return alarming_service.create_alarm_rule(rule_in, tenant_id, current_user)

@router.get("/rules", response_model=List[schemas.AlarmRule], dependencies=[Depends(require_permission("alarm_rule:read"))])
def list_alarm_rules(
    skip: int = 0,
    limit: int = 100,
    alarming_service: AlarmingService = Depends(get_alarming_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return alarming_service.list_rules(tenant_id, skip, limit)

@router.put("/rules/{rule_id}", response_model=schemas.AlarmRule, dependencies=[Depends(require_permission("alarm_rule:update"))])
def update_alarm_rule(
    rule_id: uuid.UUID,
    rule_in: schemas.AlarmRuleUpdate,
    alarming_service: AlarmingService = Depends(get_alarming_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return alarming_service.update_rule(rule_id, rule_in, tenant_id, current_user)

@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permission("alarm_rule:delete"))])
def delete_alarm_rule(
    rule_id: uuid.UUID,
    alarming_service: AlarmingService = Depends(get_alarming_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    alarming_service.delete_rule(rule_id, tenant_id, current_user)
    return None

# --- Endpoints para Alarmas Activas ---

@router.get("/alarms/active", response_model=List[schemas.Alarm], dependencies=[Depends(require_permission("alarm:read"))])
def get_active_alarms(
    alarming_service: AlarmingService = Depends(get_alarming_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return alarming_service.get_active_alarms(tenant_id)

@router.post("/alarms/{alarm_id}/acknowledge", response_model=schemas.Alarm, dependencies=[Depends(require_permission("alarm:acknowledge"))])
def acknowledge_alarm(
    alarm_id: uuid.UUID,
    alarming_service: AlarmingService = Depends(get_alarming_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    return alarming_service.acknowledge_alarm(alarm_id, tenant_id, current_user)
