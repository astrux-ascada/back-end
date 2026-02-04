# /scripts/manage_db.py
"""
Script maestro para la gestión y sembrado de la base de datos de Astruxa.

Centraliza la ejecución de todos los scripts de inicialización y datos de prueba.
Uso:
    python scripts/manage_db.py --all       # Ejecuta todo (config, usuarios, activos, historia)
    python scripts/manage_db.py --core      # Solo configuración base y usuarios
    python scripts/manage_db.py --history   # Solo datos históricos simulados
"""

import argparse
import logging
import sys
import os
import asyncio

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.db.seeding.seed_all import seed_all as seed_core_data
from scripts.seed_history import seed_history

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("manage_db")

def run_core_seeding():
    """Ejecuta la siembra de datos base (config, roles, usuarios, activos)."""
    logger.info("🚀 Iniciando siembra de datos CORE...")
    db = SessionLocal()
    try:
        seed_core_data(db)
        logger.info("✅ Datos CORE sembrados correctamente.")
    except Exception as e:
        logger.error(f"❌ Error en siembra CORE: {e}")
        db.rollback()
    finally:
        db.close()

async def run_history_seeding():
    """Ejecuta la simulación de datos históricos."""
    logger.info("⏳ Iniciando generación de HISTORIAL...")
    try:
        await seed_history()
        logger.info("✅ Historial generado correctamente.")
    except Exception as e:
        logger.error(f"❌ Error generando historial: {e}")

def main():
    parser = argparse.ArgumentParser(description="Gestor de Base de Datos de Astruxa")
    parser.add_argument("--core", action="store_true", help="Sembrar datos base (config, usuarios, activos)")
    parser.add_argument("--history", action="store_true", help="Generar datos históricos simulados")
    parser.add_argument("--all", action="store_true", help="Ejecutar TODO (Core + History)")

    args = parser.parse_args()

    if not (args.core or args.history or args.all):
        parser.print_help()
        return

    if args.core or args.all:
        run_core_seeding()

    if args.history or args.all:
        asyncio.run(run_history_seeding())

if __name__ == "__main__":
    main()
