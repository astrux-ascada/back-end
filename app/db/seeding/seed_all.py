# /app/db/seeding/seed_all.py
"""
Script de siembra maestro para la base de datos de Astruxa.

Ejecuta todos los scripts de siembra de los módulos en el orden correcto
de dependencia para poblar la base de datos con datos iniciales.
"""

import logging
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

# --- SOLUCIÓN: Importar todos los modelos aquí ---
# Esto asegura que SQLAlchemy pueda resolver todas las relaciones (mappers)
# antes de que se realice la primera consulta a la base de datos.
from app.assets.models.asset import Asset
from app.assets.models.asset_type import AssetType
from app.identity.models.user import User
from app.identity.models.role import Role
from app.identity.models.permission import Permission
from app.sectors.models import Sector
from app.configuration.models import ConfigurationParameter
from app.alarming.models import Alarm, AlarmRule

# --- Importar todos los nuevos seeders de nuestros módulos ---
from app.db.seeding._seed_configuration import seed_configuration
from app.db.seeding._seed_sectors import seed_sectors
from app.db.seeding._seed_identity import seed_identity
from app.db.seeding._seed_assets import seed_assets
from app.db.seeding._seed_core_engine import seed_core_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_all(db: Session):
    """
    Ejecuta todos los scripts de siembra en el orden correcto.
    """
    logger.info("--- Iniciando Proceso de Siembra Maestro para Astruxa ---")
    
    # El orden es crucial para respetar las claves foráneas y las dependencias.
    seed_configuration(db) # Parámetros y Enums
    seed_sectors(db)       # Áreas de la planta
    seed_identity(db)      # Permisos, Roles y Usuarios
    seed_assets(db)        # Catálogo y Activos Físicos
    seed_core_engine(db)   # Conexiones a hardware
    
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
