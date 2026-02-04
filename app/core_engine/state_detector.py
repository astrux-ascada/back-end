# /app/core_engine/state_detector.py
"""
Módulo para la detección y gestión del estado operacional de los activos.
"""
import logging
from typing import Dict
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from app.telemetry.schemas import SensorReadingCreate
from app.core_engine.models import MachineStateHistory

logger = logging.getLogger(__name__)

# --- Constantes de Estado ---
MACHINE_STATE_RUNNING = "RUNNING"
MACHINE_STATE_STOPPED = "STOPPED"
MACHINE_STATE_UNKNOWN = "UNKNOWN"

# --- Reglas de Detección (Simplificadas) ---
STOPPAGE_THRESHOLD = 10.0
RELEVANT_METRIC_FOR_STATE = "process_speed"


class StateDetector:
    """
    Gestiona el estado operacional de los activos, persistiendo los cambios en la BD.
    """

    def __init__(self, db: Session):
        self.db = db
        self._machine_states: Dict[UUID, str] = {}
        logger.info("Detector de estado inicializado con sesión de BD.")

    def process_reading(self, reading: SensorReadingCreate):
        """
        Procesa una lectura de sensor para detectar y persistir un cambio de estado.
        """
        if reading.metric_name.lower() != RELEVANT_METRIC_FOR_STATE:
            return

        new_state = (
            MACHINE_STATE_RUNNING
            if reading.value >= STOPPAGE_THRESHOLD
            else MACHINE_STATE_STOPPED
        )
        previous_state = self._machine_states.get(reading.asset_id, MACHINE_STATE_UNKNOWN)

        if new_state != previous_state:
            self._machine_states[reading.asset_id] = new_state
            logger.info(
                f"STATE CHANGE DETECTED for asset {reading.asset_id}: "
                f"'{previous_state}' -> '{new_state}' (based on value: {reading.value})"
            )
            self._persist_state_change(reading.asset_id, new_state)

    def _persist_state_change(self, asset_id: UUID, new_state: str):
        """
        Cierra el registro de estado anterior y crea uno nuevo.
        """
        now = datetime.now(timezone.utc)

        # 1. Encontrar y cerrar el registro de estado anterior (el que no tiene end_time)
        last_state_record = (
            self.db.query(MachineStateHistory)
            .filter(
                MachineStateHistory.asset_id == asset_id,
                MachineStateHistory.end_time == None,
            )
            .order_by(MachineStateHistory.start_time.desc())
            .first()
        )

        if last_state_record:
            last_state_record.end_time = now
            duration = now - last_state_record.start_time
            last_state_record.duration_seconds = duration.total_seconds()
            self.db.add(last_state_record)

        # 2. Crear el nuevo registro de estado
        new_state_record = MachineStateHistory(
            asset_id=asset_id,
            state=new_state,
            start_time=now,
        )
        self.db.add(new_state_record)
        
        try:
            self.db.commit()
        except Exception as e:
            logger.error(f"Error al persistir cambio de estado para el activo {asset_id}: {e}")
            self.db.rollback()


    def get_current_state(self, asset_id: UUID) -> str:
        """Devuelve el último estado conocido de un activo."""
        return self._machine_states.get(asset_id, MACHINE_STATE_UNKNOWN)
