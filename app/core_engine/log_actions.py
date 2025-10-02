# /app/core_engine/log_actions.py
"""
Funciones que se ejecutan en respuesta a eventos de log específicos.
"""

import logging
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.maintenance.service import MaintenanceService
from app.maintenance.schemas import WorkOrderCreate
from app.core_engine.repository import CoreEngineRepository

logger = logging.getLogger("app.core_engine.actions")


def handle_connector_error(details: Dict[str, Any], db: Session):
    """
    Manejador para el evento de error de conexión de un conector.

    Crea una orden de trabajo correctiva para el activo asociado.
    """
    data_source_id = details.get("data_source_id")
    if not data_source_id:
        logger.error("No se pudo crear la orden de trabajo automática: falta data_source_id en los detalles del log.")
        return

    # Necesitamos encontrar a qué activo está asociada esta fuente de datos.
    # Esta lógica podría ser más compleja en el futuro.
    # Por ahora, asumimos que la configuración del DataSource tiene el asset_id.
    core_engine_repo = CoreEngineRepository(db)
    data_source = core_engine_repo.get_data_source(data_source_id)

    if not data_source or not data_source.connection_params.get("nodes"):
        logger.error(f"No se pudo encontrar el activo para la DataSource {data_source_id}.")
        return

    # Asumimos que todos los nodos de una fuente de datos pertenecen al mismo activo.
    asset_id = data_source.connection_params["nodes"][0]["asset_id"]
    
    # Creamos la orden de trabajo
    maintenance_service = MaintenanceService(db, audit_service=None) # El audit_service no es necesario aquí
    
    work_order_in = WorkOrderCreate(
        asset_id=asset_id,
        category="CORRECTIVE",
        priority="HIGH",
        summary=f"Fallo de conexión detectado en la fuente de datos: {data_source.name}",
        description=f"Se ha detectado un error de conexión persistente ('Connection refused') con la fuente de datos {data_source.name} ({data_source_id}). Se requiere investigación por parte del equipo de mantenimiento."
    )

    # Para evitar crear órdenes duplicadas, podríamos verificar si ya existe una abierta para este problema.
    # (Lógica futura)

    maintenance_service.create_work_order(work_order_in, current_user=None) # La acción es del sistema
    logger.info(f"Orden de trabajo correctiva creada automáticamente para el activo {asset_id}.")
