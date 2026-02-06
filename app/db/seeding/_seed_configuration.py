# /app/db/seeding/_seed_configuration.py
"""
Seeder para la Configuración Global del Sistema.
"""
import logging
from sqlalchemy.orm import Session

from app.configuration.models import ConfigurationParameter

logger = logging.getLogger(__name__)

async def seed_configuration(db: Session, context: dict):
    logger.info("--- [9/9] Poblando Configuración Global ---")
    
    # Parámetro de ejemplo
    param = db.query(ConfigurationParameter).filter(ConfigurationParameter.key == "system_maintenance_mode").first()
    if not param:
        param = ConfigurationParameter(
            key="system_maintenance_mode",
            value="false",
            description="Pone el sistema en modo mantenimiento.",
            is_editable=True,
            is_active=True
        )
        db.add(param)
        db.commit()
