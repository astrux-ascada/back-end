# /app/reporting/stoppage_service.py
"""
Servicio para calcular KPIs y reportes de paradas.
"""
import logging
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.core_engine.models import MachineStateHistory
from app.core_engine.state_detector import MACHINE_STATE_STOPPED
from app.reporting.schemas import StoppageKpisDTO, StoppageEventDTO

logger = logging.getLogger(__name__)

class StoppageService:
    def __init__(self, db: Session):
        self.db = db

    def get_stoppage_kpis(
        self, asset_id: UUID, start_time: datetime, end_time: datetime
    ) -> StoppageKpisDTO:
        """
        Calcula los KPIs de paradas para un activo en un período de tiempo.
        """
        total_period_seconds = (end_time - start_time).total_seconds()
        if total_period_seconds <= 0:
            raise ValueError("El período de tiempo debe ser positivo.")

        # 1. Obtener todos los eventos de parada en el rango de tiempo
        stoppage_events_query = self.db.query(MachineStateHistory).filter(
            MachineStateHistory.asset_id == asset_id,
            MachineStateHistory.state == MACHINE_STATE_STOPPED,
            MachineStateHistory.start_time < end_time,
            MachineStateHistory.end_time != None,
            MachineStateHistory.end_time > start_time,
        )
        
        stoppage_events = stoppage_events_query.all()

        # 2. Calcular KPIs
        total_stoppages = len(stoppage_events)
        total_stoppage_duration_seconds = sum(event.duration_seconds for event in stoppage_events if event.duration_seconds)

        # Disponibilidad = (Tiempo Total - Tiempo Parado) / Tiempo Total
        availability = (total_period_seconds - total_stoppage_duration_seconds) / total_period_seconds
        
        # MTBF = (Tiempo Total - Tiempo Parado) / Número de Paradas
        # Solo se calcula si hay al menos una parada para evitar división por cero.
        mtbf_hours = None
        if total_stoppages > 0:
            operating_time_seconds = total_period_seconds - total_stoppage_duration_seconds
            mtbf_seconds = operating_time_seconds / total_stoppages
            mtbf_hours = mtbf_seconds / 3600

        # 3. Mapear a DTOs
        stoppage_event_dtos = [StoppageEventDTO.from_orm(event) for event in stoppage_events]

        return StoppageKpisDTO(
            asset_id=asset_id,
            total_stoppages=total_stoppages,
            total_stoppage_duration_seconds=total_stoppage_duration_seconds,
            availability=availability,
            mtbf=mtbf_hours,
            stoppage_events=stoppage_event_dtos,
        )
