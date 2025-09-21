# /app/core_engine/service.py
"""
Capa de Servicio para el módulo Core Engine.

Contiene la lógica de negocio para gestionar las fuentes de datos y la comunicación
en tiempo real con el hardware de la planta.
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
import uuid
from sqlalchemy.orm import Session

from app.core_engine import models, schemas
from app.core_engine.repository import CoreEngineRepository
from app.core_engine.connectors.opcua_connector import OpcUaConnector
from app.telemetry.service import TelemetryService
from app.telemetry.schemas import SensorReadingCreate

logger = logging.getLogger("app.core_engine.service")


class CoreEngineService:
    """Servicio de negocio para la gestión del motor de comunicación."""

    def __init__(self, db: Session, telemetry_service: TelemetryService):
        self.db = db
        self.telemetry_service = telemetry_service
        self.core_engine_repo = CoreEngineRepository(self.db)
        self._running_connectors: Dict[uuid.UUID, Any] = {}

    async def start(self):
        """Inicia el motor, creando un worker para cada fuente de datos activa."""
        logger.info("Iniciando Core Engine Service...")
        active_data_sources = self.core_engine_repo.list_active_data_sources()
        logger.info(f"Se encontraron {len(active_data_sources)} fuentes de datos activas para monitorear.")

        for ds in active_data_sources:
            if ds.protocol.upper() == "OPCUA":
                connector = OpcUaConnector(ds, self._telemetry_callback)
                await connector.start()
                self._running_connectors[ds.id] = connector
            # elif ds.protocol.upper() == "MODBUS_TCP":
            #     # Lógica futura para el conector Modbus
            #     pass
            else:
                logger.warning(f"Protocolo '{ds.protocol}' no soportado para la fuente de datos: {ds.name}")

    async def stop(self):
        """Detiene todos los conectores de monitoreo de forma segura."""
        logger.info("Deteniendo Core Engine Service...")
        for data_source_id, connector in self._running_connectors.items():
            logger.info(f"Deteniendo conector para la fuente de datos ID: {data_source_id}")
            await connector.stop()
        logger.info("Todos los conectores del Core Engine han sido detenidos.")

    def _telemetry_callback(self, data: List[SensorReadingCreate]):
        """Callback para que los conectores envíen datos al servicio de telemetría."""
        try:
            self.telemetry_service.ingest_bulk_readings(data)
            logger.debug(f"{len(data)} lecturas de telemetría procesadas.")
        except Exception as e:
            logger.error(f"Error en el callback de telemetría: {e}", exc_info=True)

    # --- Métodos de Configuración (CRUD) ---

    def create_data_source(self, data_source_in: schemas.DataSourceCreate) -> models.DataSource:
        return self.core_engine_repo.create_data_source(data_source_in)

    def get_data_source(self, data_source_id: uuid.UUID) -> Optional[models.DataSource]:
        return self.core_engine_repo.get_data_source(data_source_id)

    def list_data_sources(self, skip: int = 0, limit: int = 100) -> List[models.DataSource]:
        return self.core_engine_repo.list_data_sources(skip, limit)
