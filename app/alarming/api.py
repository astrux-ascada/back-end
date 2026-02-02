# /app/alarming/api.py
"""
API Router para el módulo de Alarming.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.alarming.schemas import AlarmRead
from app.alarming.service import AlarmingService
from app.dependencies.services import get_alarming_service
from app.dependencies.auth import get_current_active_user
from app.identity.models import User

router = APIRouter(prefix="/alarming", tags=["Alarming"])


@router.get(
    "/active",
    summary="Listar todas las alarmas activas (no reconocidas)",
    response_model=List[AlarmRead],
)
def list_active_alarms(
    alarming_service: AlarmingService = Depends(get_alarming_service),
    current_user: User = Depends(get_current_active_user),
):
    """
    Devuelve una lista de todas las alarmas que están actualmente activas y
    no han sido reconocidas.
    """
    return alarming_service.list_active_alarms()


@router.post(
    "/{alarm_id}/acknowledge",
    summary="Reconocer una alarma activa",
    response_model=AlarmRead,
)
def acknowledge_alarm(
    alarm_id: UUID,
    alarming_service: AlarmingService = Depends(get_alarming_service),
    current_user: User = Depends(get_current_active_user),
):
    """
    Marca una alarma como reconocida. Esto la elimina de la lista de alarmas activas.
    """
    alarm = alarming_service.acknowledge_alarm(alarm_id, current_user)
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarma no encontrada o ya reconocida.")
    return alarm
