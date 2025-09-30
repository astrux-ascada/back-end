# /app/db/seeding/seed_all.py
"""
Script de siembra maestro para la base de datos de Astruxa.

Ejecuta todos los scripts de siembra de los módulos en el orden correcto
de dependencia para poblar la base de datos con datos iniciales.
"""

import logging
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
# --- MEJORA: Usar importación absoluta para evitar errores de resolución ---
from app.db.seeding._seed_core_engine import seed_core_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_all(db: Session):
    """
    Ejecuta todos los scripts de siembra en el orden correcto.
    """
    logger.info("--- Iniciando Proceso de Siembra Maestro para Astruxa ---")
    
    seed_core_engine(db)
    
    logger.info("--- Proceso de Siembra Maestro Finalizado ---")


if __name__ == "__main__":
    logger.info("Ejecutando el script de siembra maestro...")
    db_session = SessionLocal()
    try:
        seed_all(db_session)
        db_session.commit()
        logger.info("Siembra maestra completada con éxito.")
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado durante la siembra maestra: {e}", exc_info=True)
        db_session.rollback()
    finally:
        db_session.close()
    logger.info("Script de siembra maestro finalizado.")
