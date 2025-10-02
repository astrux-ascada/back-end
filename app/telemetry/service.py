# /app/telemetry/service.py
"""
Capa de Servicio para el módulo de Telemetría.

Orquesta la lógica de negocio para la ingesta, consulta y evaluación de datos de telemetría.
"""

from typing import List
import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.telemetry import schemas
from app.telemetry.repository import TelemetryRepository
from app.auditing.service import AuditService
from app.identity.models import User
# --- MEJORA: Importar el servicio de alertas para la evaluación de datos ---
from app.alarming.service import AlarmingService


class TelemetryService:
    """Servicio de negocio para la gestión de la telemetría."""

    def __init__(self, db: Session, audit_service: AuditService, alarming_service: AlarmingService):
        self.db = db
        self.audit_service = audit_service
        self.alarming_service = alarming_service
        self.telemetry_repo = TelemetryRepository(self.db)

    def ingest_bulk_readings(self, readings_in: List[schemas.SensorReadingCreate]) -> int:
        """
        Ingesta un lote de lecturas de sensores y luego las evalúa contra las reglas de alerta.
        """
        # 1. Guardar los datos en la base de datos
        inserted_count = self.telemetry_repo.create_bulk_readings(readings_in)

        # 2. Evaluar cada nueva lectura contra las reglas de alerta activas
        if inserted_count > 0:
            for reading in readings_in:
                self.alarming_service.evaluate_reading(reading)
        
        return inserted_count

    def get_aggregated_readings(
        self,
        asset_id: uuid.UUID,
        metric_name: str,
        start_time: datetime,
        end_time: datetime,
        bucket_interval: str,
        current_user: User,
    ) -> List[schemas.AggregatedReadingDTO]:
        """
        Obtiene datos agregados del repositorio, registra la consulta en la auditoría
        y los mapea a una lista de DTOs.
        """
        raw_results = self.telemetry_repo.get_aggregated_readings_for_asset(
            asset_id=asset_id,
            metric_name=metric_name,
            start_time=start_time,
            end_time=end_time,
            bucket_interval=bucket_interval,
        )

        # Registrar la operación de consulta en la auditoría
        self.audit_service.log_operation(
            user=current_user,
            action="QUERY_TELEMETRY",
            entity_type="Asset",
            entity_id=asset_id,
            details={
                "metric_name": metric_name,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "interval": bucket_interval
            }
        )

        return [schemas.AggregatedReadingDTO.from_orm(row) for row in raw_results]
