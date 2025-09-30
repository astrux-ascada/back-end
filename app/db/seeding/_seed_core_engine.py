# /app/db/seeding/_seed_core_engine.py
"""
Siembra la configuración de DataSource para conectar el PLC simulado
a un activo existente en la base de datos.
"""

import logging
from sqlalchemy.orm import Session

from app.core_engine.models import DataSource
from app.assets.models import Asset

logger = logging.getLogger(__name__)

def seed_core_engine(db: Session):
    """
    Crea una configuración de DataSource para el PLC simulado, vinculándola
    a la prensa de la Línea 1 si no existe ya una DataSource para el simulador.
    """
    logger.info("Iniciando siembra de datos para el Core Engine...")

    # No creamos nuevos activos, los buscamos de los que ya han sido sembrados.
    press_line_1 = db.query(Asset).filter(Asset.serial_number == "SCH-L1-001").first()

    if not press_line_1:
        logger.error("No se pudo encontrar el activo 'Prensa Línea 1' (SCH-L1-001) para la siembra del Core Engine. Asegúrese de que el seeder de activos se haya ejecutado primero.")
        return

    # Crear la DataSource para conectar con el PLC simulado
    data_source = db.query(DataSource).filter(DataSource.name == "PLC Simulator").first()
    if not data_source:
        logger.info("Creando DataSource 'PLC Simulator' y vinculándola a la Prensa de la Línea 1...")
        
        # Los datos de telemetría del simulador se asociarán a la prensa de la línea 1.
        connection_params = {
            "url": "opc.tcp://host.docker.internal:4840/astruxa/simulator/",
            "nodes": [
                {
                    "node_id": "ns=2;s=PLC_1.Temperature",
                    "metric_name": "temperature_celsius",
                    "asset_id": str(press_line_1.id)
                },
                {
                    "node_id": "ns=2;s=PLC_1.Pressure",
                    "metric_name": "pressure_kpa",
                    "asset_id": str(press_line_1.id)
                }
            ]
        }
        
        data_source = DataSource(
            name="PLC Simulator",
            protocol="OPCUA",
            connection_params=connection_params,
            is_active=True,
            description="Fuente de datos para el servidor OPC UA de simulación, monitoreando la Prensa de la Línea 1."
        )
        db.add(data_source)
        db.commit()
        logger.info("DataSource 'PLC Simulator' creada y activada.")
    else:
        logger.warning("La DataSource 'PLC Simulator' ya existe. Saltando siembra.")

    logger.info("Siembra de datos para el Core Engine completada.")
