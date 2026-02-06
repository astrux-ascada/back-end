# /app/db/seeding/_seed_alarming.py
"""
Seeder para el módulo de Alarmas.
"""
import logging
from sqlalchemy.orm import Session

from app.alarming.models import AlarmRule

logger = logging.getLogger(__name__)

async def seed_alarming(db: Session, context: dict):
    logger.info("--- [7/9] Poblando Alarmas ---")
    
    brazo_robotico = context["brazo_robotico"]

    # Crear Regla de Alarma de Temperatura
    rule = db.query(AlarmRule).filter(AlarmRule.metric_name == "temperature_celsius", AlarmRule.asset_id == brazo_robotico.id).first()
    if not rule:
        rule = AlarmRule(
            asset_id=brazo_robotico.id,
            metric_name="temperature_celsius",
            condition=">",
            threshold=75.0,
            severity="critical",
            is_enabled=True
        )
        db.add(rule)
        db.commit()
