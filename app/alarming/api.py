# /app/alarming/api.py
"""
API Router para el módulo de Alertas.
"""

import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from app.alarming import schemas
from app.alarming.service import AlarmingService
from app.dependencies.services import get_alarming_service
from app.dependencies.auth import get_current_active_user, get_current_admin_user # Usaremos admin para crear reglas por ahora
from app.identity.models import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alarming", tags=["Alarming"])


@router.post(
    "/rules",
    summary="[Admin] Crear una nueva Regla de Alerta",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AlarmRuleRead,
    dependencies=[Depends(get_current_admin_user)], # Protegido para Administradores
)
def create_alarm_rule(
    rule_in: schemas.AlarmRuleCreate,
    alarming_service: AlarmingService = Depends(get_alarming_service),
):
    """Crea una nueva regla de alerta para un activo y una métrica."""
    return alarming_service.create_alarm_rule(rule_in)


@router.get(
    "/alarms",
    summary="Obtener todas las Alertas Activas",
    response_model=List[schemas.AlarmRead],
    dependencies=[Depends(get_current_active_user)], # Protegido para cualquier usuario logueado
)
def list_active_alarms(alarming_service: AlarmingService = Depends(get_alarming_service)):
    """Devuelve una lista de todas las alertas que no han sido borradas (CLEARED)."""
    return alarming_service.list_active_alarms()


@router.post(
    "/alarms/{alarm_id}/acknowledge",
    summary="Acusar recibo de una Alerta",
    response_model=schemas.AlarmRead,
    dependencies=[Depends(get_current_active_user)],
)
def acknowledge_alarm(
    alarm_id: uuid.UUID,
    alarming_service: AlarmingService = Depends(get_alarming_service),
):
    """Permite a un usuario marcar una alerta como reconocida."""
    alarm = alarming_service.acknowledge_alarm(alarm_id)
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found or cannot be acknowledged.")
    return alarm
