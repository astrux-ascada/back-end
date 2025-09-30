# /app/db/seeding/_seed_core_engine.py
"""
Siembra los datos de configuración inicial para el Core Engine, incluyendo
una fuente de datos de prueba para el PLC simulado.
"""

import logging
 
import json
from sqlalchemy.orm import Session

from app.assets.models import Asset, AssetType
from app.core_engine.models import DataSource

logger = logging.getLogger(__name__)

 
def seed_core_engine(db: Session):
    """
    Crea una configuración de DataSource para el PLC simulado si no existe.
    """
    logger.info("Iniciando siembra de datos para el Core Engine...")

    # 1. Crear un AssetType para el PLC simulado
    simulated_plc_type = db.query(AssetType).filter(AssetType.name == "Simulated PLC").first()
    if not simulated_plc_type:
        logger.info("Creando AssetType 'Simulated PLC'...")
        simulated_plc_type = AssetType(
            name="Simulated PLC",
            description="Un tipo de activo para el PLC de simulación de Astruxa.",
            manufacturer="Astruxa Simulators",
            category="PLC"
        )
        db.add(simulated_plc_type)
        db.commit()
        db.refresh(simulated_plc_type)

    # 2. Crear una instancia de Asset para el PLC simulado
    simulated_asset = db.query(Asset).filter(Asset.serial_number == "SIM-PLC-001").first()
    if not simulated_asset:
        logger.info("Creando Asset 'SIM-PLC-001'...")
        simulated_asset = Asset(
            asset_type_id=simulated_plc_type.id,
            serial_number="SIM-PLC-001",
            location="Sala de Simulación",
            status="operational"
        )
        db.add(simulated_asset)
        db.commit()
        db.refresh(simulated_asset)

    # 3. Crear la DataSource para conectar con el PLC simulado
    data_source = db.query(DataSource).filter(DataSource.name == "PLC Simulator").first()
    if not data_source:
        logger.info("Creando DataSource 'PLC Simulator'...")
        connection_params = {
            "url": "opc.tcp://host.docker.internal:4840/astruxa/simulator/",
            "nodes": [
                {
                    "node_id": "ns=2;s=PLC_1.Temperature",
                    "metric_name": "temperature_celsius",
                    "asset_id": str(simulated_asset.id)
                },
                {
                    "node_id": "ns=2;s=PLC_1.Pressure",
                    "metric_name": "pressure_kpa",
                    "asset_id": str(simulated_asset.id)
                }
            ]
        }
 
        data_source = DataSource(
            name="PLC Simulator",
            protocol="OPCUA",
            connection_params=connection_params,
            is_active=True,
            description="Fuente de datos para el servidor OPC UA de simulación."
        )
        db.add(data_source)
        db.commit()
        db.refresh(data_source)
        logger.info("DataSource 'PLC Simulator' creada y activada.")
    else:
        logger.warning("La DataSource 'PLC Simulator' ya existe. Saltando siembra.")

    logger.info("Siembra de datos para el Core Engine completada.")
