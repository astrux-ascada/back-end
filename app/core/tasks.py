# /app/core/tasks.py
"""
Definición de tareas de fondo (background tasks) para la aplicación.
"""
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.maintenance.scheduler import MaintenanceScheduler
import logging

logger = logging.getLogger(__name__)

# Esta tarea se ejecutará cada hora. Para pruebas, puedes cambiarlo a `seconds=60`.
@repeat_every(seconds=60 * 60, logger=logger, wait_first=True)
def run_maintenance_scheduler():
    """
    Tarea periódica que ejecuta el motor de mantenimiento preventivo.
    """
    logger.info("Ejecutando tarea programada: Mantenimiento Preventivo.")
    db: Session = SessionLocal()
    try:
        scheduler = MaintenanceScheduler(db)
        scheduler.run_preventive_maintenance_check()
    except Exception as e:
        logger.error(f"Error durante la ejecución del scheduler de mantenimiento: {e}")
    finally:
        db.close()
