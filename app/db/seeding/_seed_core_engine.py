# /app/db/seeding/_seed_core_engine.py
"""
Siembra la configuración de DataSource para los dispositivos simulados.
"""

import logging
from sqlalchemy.orm import Session

from app.core_engine.models import DataSource
from app.assets.models import Asset

logger = logging.getLogger(__name__)

def seed_core_engine(db: Session):
    """
    Crea las configuraciones de DataSource para los simuladores OPC UA y Modbus.
    """
    logger.info("Iniciando siembra de datos para el Core Engine...")

    # --- 1. Configuración para el PLC Simulado (OPC UA) ---
    press_line_1 = db.query(Asset).filter(Asset.serial_number == "SCH-L1-001").first()
    if not press_line_1:
        logger.error("No se pudo encontrar el activo 'Prensa Línea 1' (SCH-L1-001) para la siembra del Core Engine.")
    else:
        if not db.query(DataSource).filter(DataSource.name == "PLC Simulator").first():
            logger.info("Creando DataSource 'PLC Simulator' (OPC UA)...")
            opcua_params = {
                "url": "opc.tcp://host.docker.internal:4840/astruxa/simulator/",
                "nodes": [
                    {"node_id": "ns=2;s=PLC_1.Temperature", "metric_name": "temperature_celsius", "asset_id": str(press_line_1.id)},
                    {"node_id": "ns=2;s=PLC_1.Pressure", "metric_name": "pressure_kpa", "asset_id": str(press_line_1.id)}
                ]
            }
            db.add(DataSource(name="PLC Simulator", protocol="OPCUA", connection_params=opcua_params, is_active=True))
            db.commit()
            logger.info("DataSource 'PLC Simulator' creada.")

    # --- 2. Configuración para el Tanque Simulado (Modbus) ---
    hydraulic_tank = db.query(Asset).filter(Asset.serial_number == "TNK-HYD-001").first()
    if not hydraulic_tank:
        logger.error("No se pudo encontrar el activo 'Tanque de Aceite' (TNK-HYD-001) para la siembra del Core Engine.")
    else:
        if not db.query(DataSource).filter(DataSource.name == "Tanque Principal (Modbus)").first():
            logger.info("Creando DataSource 'Tanque Principal (Modbus)'...")
            modbus_params = {
                "host": "host.docker.internal",
                "port": 5020,
                "polling_interval_seconds": 3,
                "registers": [
                    {"address": 0, "metric_name": "tank_level_liters", "asset_id": str(hydraulic_tank.id)},
                    {"address": 1, "metric_name": "valve_status", "asset_id": str(hydraulic_tank.id)}
                ]
            }
            db.add(DataSource(name="Tanque Principal (Modbus)", protocol="MODBUS", connection_params=modbus_params, is_active=True))
            db.commit()
            logger.info("DataSource 'Tanque Principal (Modbus)' creada.")

    logger.info("Siembra de datos para el Core Engine completada.")
