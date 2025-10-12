# /app/alarming/api.py
"""
API Router para la gestión de reglas de alarma y visualización de alarmas.
"""

from fastapi import APIRouter, Depends
import uuid
from typing import List

from app.alarming import schemas
from app.alarming.service import AlarmingService
from app.dependencies.services import get_alarming_service
from app.dependencies.auth import get_current_admin_user

router = APIRouter(prefix="/alarming", tags=["Alarming"], dependencies=[Depends(get_current_admin_user)])

@router.post("/rules", response_model=schemas.AlarmRule, status_code=201)
def create_alarm_rule(rule_in: schemas.AlarmRuleCreate, alarming_service: AlarmingService = Depends(get_alarming_service)):
    """Crea una nueva regla de alarma."""
    return alarming_service.create_alarm_rule(rule_in)

@router.get("/alarms/active", response_model=List[schemas.AlarmRule])
def list_active_alarms(alarming_service: AlarmingService = Depends(get_alarming_service)):
    """Obtiene una lista de todas las alarmas que están actualmente activas (no reconocidas)."""
    # Note: This should likely return a schema for Alarm, not AlarmRule. 
    # This is a placeholder to get the app running.
    return alarming_service.list_active_alarms()

@router.post("/alarms/{alarm_id}/acknowledge", response_model=schemas.AlarmRule)
def acknowledge_alarm(alarm_id: uuid.UUID, alarming_service: AlarmingService = Depends(get_alarming_service)):
    """Reconoce (marca como vista) una alarma activa."""
    # Note: This should likely return a schema for Alarm, not AlarmRule.
    # This is a placeholder to get the app running.
    return alarming_service.acknowledge_alarm(alarm_id)
