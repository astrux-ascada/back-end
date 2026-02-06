# /scripts/seed_all.py
"""
Script maestro para poblar la base de datos con TODOS los datos necesarios.
Ejecuta los scripts de seeding individuales en el orden correcto.
"""
import asyncio
import logging

from app.core.database import SessionLocal
from scripts.seed_history import seed_history
# Importar las funciones de seeding de los otros archivos
from scripts.seed_saas import seed_data as seed_saas_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    logger.info("--- Iniciando Proceso de Seeding Maestro ---")
    db = SessionLocal()
    try:
        # Ejecutar el seeder de la estructura SaaS primero
        await seed_saas_data(db)

        # Ejecutar el seeder del historial de datos después
        await seed_history(db)

        logger.info("--- Proceso de Seeding Maestro Finalizado con Éxito ---")
    except Exception as e:
        logger.error(f"Ocurrió un error durante el seeding maestro: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
