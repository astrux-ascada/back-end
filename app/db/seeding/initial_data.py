"""
Script principal para la siembra de datos iniciales en la base de datos.

Este script se puede ejecutar desde la línea de comandos para poblar
las tablas con datos esenciales después de una migración.
"""

import logging

from app.core.config import get_db
from app.db.seeding._seed_clients import seed_clients
from app.db.seeding._seed_diseases import seed_diseases
from app.db.seeding._seed_vital_signs import seed_vital_signs  # NUEVA IMPORTACIÓN

# Configuración básica de logging para ver la salida en la consola
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_all():
    """
    Función principal que orquesta la siembra de todos los datos.
    """
    logger.info("Obteniendo sesión de la base de datos para la siembra...")
    db_session = next(get_db())

    # Llama a cada función de siembra aquí
    seed_diseases(db_session)
    seed_clients(db_session)
    # --- NUEVO: Añadir la siembra de signos vitales ---
    seed_vital_signs(db_session)
    # Podrías añadir más, como: seed_admin_user(db_session)

    logger.info("✅ Proceso de siembra de datos completado exitosamente.")


if __name__ == "__main__":
    seed_all()
