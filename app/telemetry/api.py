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
# --- MEJORA: Importar dependencias de autenticación y el modelo de usuario ---
from app.dependencies.auth import get_current_active_user
from app.identity.models import User

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
    # --- MEJORA: Proteger el endpoint y obtener el usuario para la auditoría ---
    current_user: User = Depends(get_current_active_user),
):
    """
    Obtiene datos de series temporales agregados para un activo específico,
    ideal para la visualización en gráficos. La consulta queda registrada en la auditoría.
    """
    return telemetry_service.get_aggregated_readings(
        asset_id=asset_id,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        bucket_interval=bucket_interval,
        current_user=current_user,
    )
