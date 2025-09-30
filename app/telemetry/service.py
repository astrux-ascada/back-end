# /app/telemetry/service.py
"""
Capa de Servicio para el módulo de Telemetría.

Orquesta la lógica de negocio para la ingesta y consulta de datos de telemetría.
"""

from typing import List
import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.telemetry import schemas
from app.telemetry.repository import TelemetryRepository


class TelemetryService:
    """Servicio de negocio para la gestión de la telemetría."""

    def __init__(self, db: Session):
        self.db = db
        self.telemetry_repo = TelemetryRepository(self.db)

    def ingest_bulk_readings(self, readings_in: List[schemas.SensorReadingCreate]) -> int:
        """Ingesta un lote de lecturas de sensores."""
        return self.telemetry_repo.create_bulk_readings(readings_in)

    def get_aggregated_readings(
        self,
        asset_id: uuid.UUID,
        metric_name: str,
        start_time: datetime,
        end_time: datetime,
        bucket_interval: str,
    ) -> List[schemas.AggregatedReadingDTO]:
        """
        Obtiene datos agregados del repositorio y los mapea a una lista de DTOs.
        """
        raw_results = self.telemetry_repo.get_aggregated_readings_for_asset(
            asset_id=asset_id,
            metric_name=metric_name,
            start_time=start_time,
            end_time=end_time,
            bucket_interval=bucket_interval,
        )

        # Pydantic se encargará de mapear los resultados de la consulta (que tienen los mismos
        # nombres de columna que los campos del DTO) a la lista de esquemas.
        return [schemas.AggregatedReadingDTO.from_orm(row) for row in raw_results]
