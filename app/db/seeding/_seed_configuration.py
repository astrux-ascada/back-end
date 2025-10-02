# /app/db/seeding/_seed_configuration.py
"""
Script de siembra para el módulo de Configuración.

Pobla la base de datos con parámetros y enums dinámicos por defecto.
"""

import logging
from sqlalchemy.orm import Session

from app.configuration.models import ConfigurationParameter, EnumType, EnumValue

logger = logging.getLogger(__name__)

# --- Datos de Siembra Predefinidos ---

PARAMETERS_DATA = {
    "procurement.ai.provider_suggestion_count": {
        "value": "3",
        "description": "Número de proveedores que la IA debe sugerir para una cotización."
    },
    "maintenance.preventive.default_days_interval": {
        "value": "90",
        "description": "Intervalo por defecto en días para generar órdenes de mantenimiento preventivo."
    },
}

ENUMS_DATA = {
    "WorkOrderStatus": {
        "description": "Los posibles estados de una orden de trabajo.",
        "values": [
            {"value": "OPEN", "label": "Abierta", "color": "#ef4444"},
            {"value": "IN_PROGRESS", "label": "En Progreso", "color": "#3b82f6"},
            {"value": "ON_HOLD", "label": "En Espera", "color": "#f97316"},
            {"value": "COMPLETED", "label": "Completada", "color": "#22c55e"},
            {"value": "CANCELED", "label": "Cancelada", "color": "#6b7280"},
        ]
    },
    "AssetStatus": {
        "description": "Los posibles estados operativos de un activo.",
        "values": [
            {"value": "OPERATIONAL", "label": "Operacional", "color": "#22c55e"},
            {"value": "MAINTENANCE", "label": "En Mantenimiento", "color": "#f97316"},
            {"value": "FAULT", "label": "Con Fallo", "color": "#ef4444"},
            {"value": "IDLE", "label": "Inactivo", "color": "#6b7280"},
        ]
    },
}

def seed_configuration(db: Session):
    logger.info("Iniciando siembra de datos para Configuración...")

    # 1. Sembrar Parámetros de Configuración
    for key, data in PARAMETERS_DATA.items():
        if not db.query(ConfigurationParameter).filter(ConfigurationParameter.key == key).first():
            db.add(ConfigurationParameter(key=key, value=data["value"], description=data["description"]))
    db.commit()
    logger.info("Parámetros de configuración sembrados.")

    # 2. Sembrar Enums Dinámicos
    for name, data in ENUMS_DATA.items():
        enum_type = db.query(EnumType).filter(EnumType.name == name).first()
        if not enum_type:
            enum_type = EnumType(name=name, description=data["description"])
            db.add(enum_type)
            db.commit()
            db.refresh(enum_type)
            logger.info(f"EnumType creado: {name}")

        for value_data in data["values"]:
            existing_value = db.query(EnumValue).filter(EnumValue.enum_type_id == enum_type.id, EnumValue.value == value_data["value"]).first()
            if not existing_value:
                db.add(EnumValue(enum_type_id=enum_type.id, **value_data))
                logger.info(f"  - EnumValue añadido a {name}: {value_data['value']}")
    db.commit()
    logger.info("Enums dinámicos sembrados.")

    logger.info("Siembra de datos para Configuración completada.")
