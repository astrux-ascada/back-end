# /app/telemetry/api.py
"""
API Router para el módulo de Telemetría.

Define los endpoints para la ingesta y consulta de datos de series temporales.
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, status, Query

from app.telemetry import schemas
from app.telemetry.service import TelemetryService
from app.dependencies.services import get_telemetry_service

logger = logging.getLogger("app.telemetry.api")

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


@router.post(
    "/readings",
    summary="Ingesta masiva de lecturas de sensores",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.BulkIngestionResponse,
)
def ingest_sensor_readings(
    bulk_readings_in: schemas.BulkSensorReadingCreate,
    telemetry_service: TelemetryService = Depends(get_telemetry_service),
):
    """Recibe un lote de lecturas de sensores para su procesamiento."""
    processed_count = telemetry_service.ingest_bulk_readings(bulk_readings_in.readings)
    message = f"{processed_count} lecturas recibidas y encoladas para procesamiento."
    logger.info(message)
    return schemas.BulkIngestionResponse(message=message, received_count=processed_count)


@router.get(
    "/readings/{asset_id}",
    summary="Obtener datos de telemetría agregados para un activo",
    response_model=List[schemas.AggregatedReadingDTO],
)
def get_aggregated_readings(
    asset_id: uuid.UUID,
    metric_name: str,
    start_time: datetime = Query(default_factory=lambda: datetime.utcnow() - timedelta(hours=24)),
    end_time: datetime = Query(default_factory=datetime.utcnow),
    bucket_interval: str = Query("1 minute", alias="interval"),
    telemetry_service: TelemetryService = Depends(get_telemetry_service),
):
    """
    Obtiene datos de series temporales agregados para un activo específico,
    ideal para la visualización en gráficos.

    - **asset_id**: El UUID del activo a consultar.
    - **metric_name**: El nombre de la métrica (ej: 'temperature_celsius').
    - **start_time**: La fecha y hora de inicio del rango de tiempo (formato ISO 8601).
    - **end_time**: La fecha y hora de fin del rango de tiempo (formato ISO 8601).
    - **interval**: El tamaño del intervalo de agregación (ej: '1 second', '5 minutes', '1 hour').
    """
    return telemetry_service.get_aggregated_readings(
        asset_id=asset_id,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        bucket_interval=bucket_interval,
    )
