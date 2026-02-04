# /app/db/seeding/_seed_maintenance.py
"""
Script para sembrar la base de datos con datos de Mantenimiento (Planes Preventivos).
"""
import logging
from sqlalchemy.orm import Session
from app.maintenance.models import MaintenancePlan, MaintenancePlanTask
from app.assets.models import Asset

logger = logging.getLogger(__name__)

def seed_maintenance(db: Session):
    """
    Crea planes de mantenimiento preventivo de ejemplo.
    """
    logger.info("Iniciando siembra de datos para Mantenimiento...")

    # Obtener el activo de la máquina cartonera
    cartonera_asset = db.query(Asset).filter(Asset.serial_number == "CARTONERA-MQ-01").first()
    if not cartonera_asset:
        logger.warning("No se encontró el activo 'CARTONERA-MQ-01'. No se crearán planes de mantenimiento.")
        return

    # --- 1. Crear Plan de Mantenimiento Semanal ---
    plan_name = "Revisión Semanal de la Cartonera"
    if not db.query(MaintenancePlan).filter_by(name=plan_name).first():
        plan = MaintenancePlan(
            name=plan_name,
            description="Plan de mantenimiento preventivo para la máquina cartonera, a realizarse cada 7 días.",
            asset_id=cartonera_asset.id,
            summary_template="Revisión Preventiva Semanal - Cartonera",
            category="PREVENTIVE",
            priority="MEDIUM",
            trigger_type="TIME_BASED",
            interval_days=7,
            is_active=True
        )
        db.add(plan)
        logger.info(f"Creando plan: {plan.name}")

        # --- 2. Añadir Tareas al Plan ---
        tasks_data = [
            {"description": "Verificar y limpiar sensores ópticos", "order": 1},
            {"description": "Inspeccionar correas de transmisión", "order": 2},
            {"description": "Verificar niveles de lubricante", "order": 3},
            {"description": "Comprobar paradas de emergencia", "order": 4},
        ]
        
        # Necesitamos el ID del plan, así que hacemos commit aquí
        db.commit()
        db.refresh(plan)

        for task_data in tasks_data:
            task = MaintenancePlanTask(plan_id=plan.id, **task_data)
            db.add(task)
        
        db.commit()

    logger.info("Siembra de datos para Mantenimiento completada.")
