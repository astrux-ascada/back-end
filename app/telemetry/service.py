# /app/telemetry/service.py
"""
Capa de Servicio para el módulo de Telemetría.

Orquesta la lógica de negocio para la ingesta y procesamiento de datos de telemetría.
"""

from typing import List
from sqlalchemy.orm import Session

from app.telemetry import schemas
from app.telemetry.repository import TelemetryRepository


class TelemetryService:
    """Servicio de negocio para la gestión de la telemetría."""

    def __init__(self, db: Session):
        self.db = db
        self.telemetry_repo = TelemetryRepository(self.db)

    def ingest_bulk_readings(self, readings_in: List[schemas.SensorReadingCreate]) -> int:
        """
        Ingesta un lote de lecturas de sensores.

        Por ahora, delega directamente en el repositorio. En el futuro, aquí se
        implementará la lógica de validación, alertas y publicación de eventos.

        Returns:
            El número de lecturas procesadas.
        """
        # Lógica de negocio futura:
        # 1. Validar que los asset_id existen.
        # 2. Comprobar si algún valor supera los umbrales de alerta.
        # 3. Publicar un evento en RabbitMQ.

        return self.telemetry_repo.create_bulk_readings(readings_in)
