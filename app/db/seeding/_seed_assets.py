# /app/db/seeding/_seed_assets.py
"""
Script de siembra para el módulo de Activos (AssetTypes, AssetHierarchy, Assets).
"""

import logging
from sqlalchemy.orm import Session

from app.assets.models import Asset, AssetType, AssetHierarchy
from app.sectors.models import Sector

logger = logging.getLogger(__name__)

# --- Datos de Siembra Predefinidos ---

ASSET_TYPES_DATA = {
    # Machines & Robots
    "Prensa Hidráulica Schuler 500T": {"category": "MACHINE"},
    "Brazo Robótico KUKA KR 210": {"category": "ROBOT"},
    # --- MEJORA: Añadir tipo de activo para el simulador Modbus ---
    "Tanque de Aceite Hidráulico": {"category": "EQUIPMENT"},
    # Sensors
    "Cámara de Visión Cognex-1000": {"category": "SENSOR"},
    "Sensor de Temperatura IFM-T2": {"category": "SENSOR"},
    "Sensor de Presión Bosch-P1": {"category": "SENSOR"},
    # PLCs & Components
    "PLC Siemens S7-1500": {"category": "PLC"},
    "Motor Eléctrico 150kW": {"category": "COMPONENT"},
    "Bomba Hidráulica Rexroth": {"category": "COMPONENT"},
}

ASSET_HIERARCHY_DATA = [
    {"parent": "Prensa Hidráulica Schuler 500T", "child": "PLC Siemens S7-1500", "quantity": 1},
    {"parent": "Prensa Hidráulica Schuler 500T", "child": "Bomba Hidráulica Rexroth", "quantity": 2},
    {"parent": "Brazo Robótico KUKA KR 210", "child": "PLC Siemens S7-1500", "quantity": 1},
    {"parent": "Brazo Robótico KUKA KR 210", "child": "Motor Eléctrico 150kW", "quantity": 6},
]

ASSETS_DATA = [
    # Línea 1
    {"type": "Prensa Hidráulica Schuler 500T", "serial": "SCH-L1-001", "sector": "Línea de Estampado 1"},
    {"type": "Brazo Robótico KUKA KR 210", "serial": "KUK-L1-001", "sector": "Línea de Estampado 1"},
    {"type": "Cámara de Visión Cognex-1000", "serial": "COG-L1-001", "sector": "Línea de Estampado 1"},
    # Línea 2
    {"type": "Prensa Hidráulica Schuler 500T", "serial": "SCH-L2-001", "sector": "Línea de Estampado 2"},
    {"type": "Brazo Robótico KUKA KR 210", "serial": "KUK-L2-001", "sector": "Línea de Estampado 2"},
    {"type": "Cámara de Visión Cognex-1000", "serial": "COG-L2-001", "sector": "Línea de Estampado 2"},
    # --- MEJORA: Añadir instancia de activo para el simulador Modbus ---
    {"type": "Tanque de Aceite Hidráulico", "serial": "TNK-HYD-001", "sector": "Área de Mantenimiento"},
]

def seed_assets(db: Session):
    logger.info("Iniciando siembra de datos para Activos...")

    # 1. Sembrar AssetTypes
    for name, data in ASSET_TYPES_DATA.items():
        if not db.query(AssetType).filter(AssetType.name == name).first():
            db.add(AssetType(name=name, category=data["category"]))
    db.commit()
    logger.info("Tipos de Activos (AssetTypes) sembrados.")

    # 2. Sembrar AssetHierarchy
    for item in ASSET_HIERARCHY_DATA:
        parent_type = db.query(AssetType).filter(AssetType.name == item["parent"]).one()
        child_type = db.query(AssetType).filter(AssetType.name == item["child"]).one()
        
        existing_link = db.query(AssetHierarchy).filter_by(parent_asset_type_id=parent_type.id, child_asset_type_id=child_type.id).first()
        if not existing_link:
            db.add(AssetHierarchy(parent_asset_type_id=parent_type.id, child_asset_type_id=child_type.id, quantity=item["quantity"]))
    db.commit()
    logger.info("Jerarquía de Activos (AssetHierarchy) sembrada.")

    # 3. Sembrar Assets
    for item in ASSETS_DATA:
        if not db.query(Asset).filter(Asset.serial_number == item["serial"]).first():
            asset_type = db.query(AssetType).filter(AssetType.name == item["type"]).one()
            sector = db.query(Sector).filter(Sector.name == item["sector"]).one()
            db.add(Asset(asset_type_id=asset_type.id, serial_number=item["serial"], sector_id=sector.id, location=sector.name))
    db.commit()
    logger.info("Activos (Assets) sembrados.")

    logger.info("Siembra de datos para Activos completada.")
