# /app/telemetry/api.py
"""
API Router para el módulo de Telemetría.

Define el endpoint para la ingesta masiva de lecturas de sensores.
"""

import logging

from fastapi import APIRouter, Depends, status

from app.telemetry import schemas
from app.telemetry.service import TelemetryService
# --- MEJORA: Importamos el inyector de dependencias desde la ubicación central ---
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
    """
    Recibe un lote de lecturas de sensores y las envía al servicio de telemetría
    para su procesamiento y almacenamiento.
    """
    processed_count = telemetry_service.ingest_bulk_readings(bulk_readings_in.readings)
    message = f"{processed_count} lecturas recibidas y encoladas para procesamiento."
    logger.info(message)
    return schemas.BulkIngestionResponse(message=message, received_count=processed_count)
