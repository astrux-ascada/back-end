# /app/db/seeding/seed_all.py

import logging
import random
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import SessionLocal
from app.models.client import Client
from ._seed_diseases import seed_diseases
from ._seed_clients import seed_clients
from ._seed_addictions import seed_addictions_for_user
from ._seed_menstrual_cycle import seed_menstrual_cycle_for_user
from ._seed_pregnancy import seed_pregnancy_for_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_all(db: Session):
    """
    Ejecuta todos los scripts de siembra en el orden correcto de dependencia.
    Selecciona usuarios de prueba dinámicamente para poblar datos específicos.
    """
    logger.info("--- Iniciando Proceso de Siembra Maestro ---")
    fake = Faker("es_ES")

    # 1. Sembrar datos maestros y clientes base
    seed_diseases(db)
    seed_clients(db)

    # --- INICIO DE LA SOLUCIÓN: Selección dinámica de usuarios ---
    logger.info("--- Iniciando siembra de datos para usuarios de prueba seleccionados dinámicamente ---")

    # 2. Seleccionar un usuario femenino aleatorio para datos específicos
    female_user = db.query(Client).filter(Client.sex == 'F').order_by(func.random()).first()

    if female_user:
        logger.info(f"Poblando datos de ciclo menstrual y embarazo para: {female_user.email}")
        seed_menstrual_cycle_for_user(db, female_user, fake)
        seed_pregnancy_for_user(db, female_user, fake)
    else:
        logger.warning("No se encontró un usuario femenino para la siembra de datos específicos.")

    # 3. Seleccionar dos usuarios aleatorios (cualquier género) para datos generales
    # Nos aseguramos de no seleccionar al mismo usuario dos veces si es posible
    users_for_general_data = db.query(Client).order_by(func.random()).limit(2).all()
    
    if users_for_general_data:
        for user in users_for_general_data:
            logger.info(f"Poblando datos generales (adicciones) para: {user.email}")
            seed_addictions_for_user(db, user, fake)
    else:
        logger.warning("No se encontraron usuarios para la siembra de datos generales.")
    # --- FIN DE LA SOLUCIÓN ---


if __name__ == "__main__":
    logger.info("Ejecutando el script de siembra maestro...")
    db_session = SessionLocal()
    try:
        seed_all(db_session)
        db_session.commit()
        logger.info("--- Proceso de Siembra Maestro Finalizado con Éxito ---")
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado durante la siembra maestra: {e}", exc_info=True)
        db_session.rollback()
    finally:
        db_session.close()
    logger.info("Script de siembra maestro finalizado.")
