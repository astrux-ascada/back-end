# /app/alarming/api.py
"""
API Router para el módulo de Alarming.
"""

from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.alarming.schemas import AlarmRead
from app.alarming.service import AlarmingService
from app.dependencies.services import get_alarming_service
from app.dependencies.auth import get_current_active_user # Cambiado a active_user para que más roles puedan ver
from app.dependencies.tenant import get_tenant_id

router = APIRouter(prefix="/alarming", tags=["Alarming"], dependencies=[Depends(get_current_active_user)])

@router.post("/rules", response_model=schemas.AlarmRule, status_code=201)
def create_alarm_rule(
    rule_in: schemas.AlarmRuleCreate, 
    alarming_service: AlarmingService = Depends(get_alarming_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """Crea una nueva regla de alarma para el tenant actual."""
    try:
        return alarming_service.create_alarm_rule(rule_in, tenant_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/alarms/active", response_model=List[schemas.Alarm])
def list_active_alarms(
    alarming_service: AlarmingService = Depends(get_alarming_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """Obtiene una lista de todas las alarmas activas del tenant actual."""
    return alarming_service.list_active_alarms(tenant_id)


@router.post("/alarms/{alarm_id}/acknowledge", response_model=schemas.Alarm)
def acknowledge_alarm(
    alarm_id: uuid.UUID, 
    alarming_service: AlarmingService = Depends(get_alarming_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """Reconoce (marca como vista) una alarma activa del tenant actual."""
    alarm = alarming_service.acknowledge_alarm(alarm_id, tenant_id)
    if not alarm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alarm not found")
    return alarm
