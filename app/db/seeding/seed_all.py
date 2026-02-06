# /app/db/seeding/seed_all.py
"""
Script maestro para poblar la base de datos con TODOS los datos de ejemplo.
"""
import asyncio
import logging
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.db.seeding.initial_data import seed_initial_data
from app.db.seeding._seed_identity import seed_identity
from app.db.seeding._seed_sectors import seed_sectors
from app.db.seeding._seed_assets import seed_assets
from app.db.seeding._seed_procurement import seed_procurement
from app.db.seeding._seed_maintenance import seed_maintenance
from app.db.seeding._seed_alarming import seed_alarming
from app.db.seeding._seed_core_engine import seed_core_engine
from app.db.seeding._seed_configuration import seed_configuration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_all_data(db: Session):
    logger.info("--- Iniciando Proceso de Seeding Maestro ---")
    
    # El orden es crucial para respetar las dependencias (ej: crear usuarios antes de asignarles tareas)
    
    logger.info("1. Poblando datos iniciales (Planes, Permisos, Super Admin)...")
    initial_data = await seed_initial_data(db)
    
    logger.info("2. Poblando datos de Identidad (Usuarios y Roles de demo)...")
    await seed_identity(db, initial_data)
    
    logger.info("3. Poblando Sectores...")
    await seed_sectors(db, initial_data)
    
    logger.info("4. Poblando Activos...")
    await seed_assets(db, initial_data)
    
    logger.info("5. Poblando datos de Compras (Proveedores, Repuestos)...")
    await seed_procurement(db, initial_data)
    
    logger.info("6. Poblando datos de Mantenimiento (Órdenes de Trabajo)...")
    await seed_maintenance(db, initial_data)
    
    logger.info("7. Poblando datos de Alarmas...")
    await seed_alarming(db, initial_data)
    
    logger.info("8. Poblando Core Engine (Fuentes de Datos)...")
    await seed_core_engine(db, initial_data)
    
    logger.info("9. Poblando Configuración...")
    await seed_configuration(db, initial_data)

    logger.info("--- Proceso de Seeding Maestro Finalizado con Éxito ---")

async def main():
    db = SessionLocal()
    try:
        await seed_all_data(db)
    except Exception as e:
        logger.error(f"Ocurrió un error durante el seeding maestro: {e}", exc_info=True)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
