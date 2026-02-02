# /app/db/seeding/seed_all.py
"""
Script de siembra maestro para la base de datos de Astruxa.
"""

import logging
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

# --- Importar todos los modelos para que Alembic los vea ---
from app.assets.models import *
from app.identity.models import *
from app.sectors.models import *
from app.configuration.models import *
from app.alarming.models import *
from app.telemetry.models import *
from app.core_engine.models import *
from app.notifications.models import *
from app.procurement.models import *
from app.maintenance.models import *

# --- Importar todos los seeders de nuestros módulos ---
from ._seed_configuration import seed_configuration
from ._seed_sectors import seed_sectors
from ._seed_identity import seed_identity
from ._seed_assets import seed_assets
from ._seed_core_engine import seed_core_engine
from ._seed_alarming import seed_alarming
from ._seed_procurement import seed_procurement
from ._seed_maintenance import seed_maintenance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_all(db: Session):
    """
    Ejecuta todos los scripts de siembra en el orden correcto.
    """
    logger.info("--- Iniciando Proceso de Siembra Maestro para Astruxa ---")
    
    # El orden es crucial para respetar las claves foráneas y las dependencias.
    seed_configuration(db)
    seed_sectors(db)
    seed_identity(db)
    seed_assets(db)
    seed_core_engine(db)
    seed_alarming(db)
    seed_procurement(db)
    seed_maintenance(db)
    
    logger.info("--- Proceso de Siembra Maestro Finalizado ---")


if __name__ == "__main__":
    logger.info("Ejecutando el script de siembra maestro...")
    db_session = SessionLocal()
    try:
        seed_all(db_session)
        logger.info("Siembra maestra completada con éxito.")
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado durante la siembra maestra: {e}", exc_info=True)
        db_session.rollback()
    finally:
        db_session.close()
    logger.info("Script de siembra maestro finalizado.")
