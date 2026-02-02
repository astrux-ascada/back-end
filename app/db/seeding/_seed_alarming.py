# /app/db/seeding/_seed_alarming.py
"""
Script para sembrar la base de datos con reglas de alarma de ejemplo.
"""
import logging
from sqlalchemy.orm import Session
from app.alarming.models import AlarmRule
from app.assets.models import Asset

logger = logging.getLogger(__name__)

def seed_alarming(db: Session):
    """
    Crea reglas de alarma para los activos existentes.
    """
    logger.info("Iniciando siembra de datos para Alarmas...")

    # Obtener el activo de la máquina cartonera
    cartonera_asset = db.query(Asset).filter(Asset.serial_number == "CARTONERA-MQ-01").first()

    if not cartonera_asset:
        logger.warning("No se encontró el activo 'CARTONERA-MQ-01'. No se crearán reglas de alarma.")
        return

    # Reglas de alarma para la máquina cartonera
    alarm_rules_data = [
        {
            "asset_id": cartonera_asset.id,
            "metric_name": "process_speed",
            "condition": "<",
            "threshold": 15.0,
            "severity": "warning",
            "is_enabled": True,
        },
        {
            "asset_id": cartonera_asset.id,
            "metric_name": "process_speed",
            "condition": "<",
            "threshold": 5.0,
            "severity": "critical",
            "is_enabled": True,
        },
        # Regla para temperatura alta (para probar integración con mantenimiento)
        {
            "asset_id": cartonera_asset.id,
            "metric_name": "temperature",
            "condition": ">",
            "threshold": 80.0,
            "severity": "critical",
            "is_enabled": True,
        }
    ]

    for rule_data in alarm_rules_data:
        # Evitar duplicados
        exists = db.query(AlarmRule).filter_by(
            asset_id=rule_data["asset_id"],
            metric_name=rule_data["metric_name"],
            condition=rule_data["condition"],
            threshold=rule_data["threshold"],
        ).first()

        if not exists:
            db.add(AlarmRule(**rule_data))
            logger.info(f"Creando regla de alarma: {rule_data['metric_name']} {rule_data['condition']} {rule_data['threshold']}")

    db.commit()
    logger.info("Siembra de datos para Alarmas completada.")
