# /app/telemetry/repository.py
"""
Capa de Repositorio para el módulo de Telemetría.

Optimizado para la inserción masiva y la consulta agregada de datos de series temporales.
"""

from typing import List, Any
import uuid
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, label

from app.telemetry import models, schemas


class TelemetryRepository:
    """Realiza operaciones CRUD y de consulta en la base de datos para la telemetría."""

    def __init__(self, db: Session):
        self.db = db

    def create_bulk_readings(self, readings_in: List[schemas.SensorReadingCreate]) -> int:
        """Inserta una lista de lecturas de sensores en la base de datos de forma masiva."""
        db_readings_data = [r.model_dump() for r in readings_in]
        db_objects = [models.SensorReading(**data) for data in db_readings_data]
        self.db.add_all(db_objects)
        self.db.commit()
        return len(db_objects)

    def get_aggregated_readings_for_asset(
        self,
        asset_id: uuid.UUID,
        metric_name: str,
        start_time: datetime,
        end_time: datetime,
        bucket_interval: str,
    ) -> List[Any]:
        """
        Obtiene datos de telemetría agregados para un activo y una métrica específicos.

        Utiliza la función `time_bucket` de TimescaleDB para agrupar los datos en intervalos.
        """
        bucket = label("bucket", func.time_bucket(bucket_interval, models.SensorReading.timestamp))

        query = (
            self.db.query(
                bucket,
                label("avg_value", func.avg(models.SensorReading.value)),
                label("min_value", func.min(models.SensorReading.value)),
                label("max_value", func.max(models.SensorReading.value)),
            )
            .filter(
                models.SensorReading.asset_id == asset_id,
                models.SensorReading.metric_name == metric_name,
                models.SensorReading.timestamp >= start_time,
                models.SensorReading.timestamp <= end_time,
            )
            .group_by(bucket)
            .order_by(bucket)
        )

        return query.all()
