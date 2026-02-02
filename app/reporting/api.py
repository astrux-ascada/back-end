# /app/reporting/api.py
"""
API Router para el módulo de Reporting.
"""
from uuid import UUID
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query

from app.reporting.schemas import MachineStateDTO, StoppageKpisDTO
from app.reporting.service import ReportingService
from app.reporting.stoppage_service import StoppageService
from app.dependencies.services import get_reporting_service, get_stoppage_service
from app.dependencies.auth import get_current_active_user
from app.identity.models import User

router = APIRouter(prefix="/reporting", tags=["Reporting"])


@router.get(
    "/machine-state/{asset_id}",
    summary="Obtener el estado actual de una máquina",
    response_model=MachineStateDTO,
)
def get_machine_state(
    asset_id: UUID,
    reporting_service: ReportingService = Depends(get_reporting_service),
    current_user: User = Depends(get_current_active_user),
):
    """
    Devuelve el estado operacional actual (RUNNING/STOPPED) de una máquina específica.
    Requiere autenticación.
    """
    return reporting_service.get_machine_state(asset_id)


@router.get(
    "/stoppage-kpis/{asset_id}",
    summary="Obtener KPIs de paradas para un activo",
    response_model=StoppageKpisDTO,
)
def get_stoppage_kpis(
    asset_id: UUID,
    start_time: datetime = Query(default_factory=lambda: datetime.now() - timedelta(days=1)),
    end_time: datetime = Query(default_factory=datetime.now),
    stoppage_service: StoppageService = Depends(get_stoppage_service),
    current_user: User = Depends(get_current_active_user),
):
    """
    Calcula y devuelve los KPIs de paradas (disponibilidad, MTBF, etc.)
    para un activo en un período de tiempo determinado. Requiere autenticación.
    """
    try:
        return stoppage_service.get_stoppage_kpis(
            asset_id=asset_id, start_time=start_time, end_time=end_time
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
