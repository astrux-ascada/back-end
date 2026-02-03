# /app/maintenance/scheduler.py
"""
Motor de programación para el Mantenimiento Preventivo.
Se encarga de evaluar los planes y generar órdenes de trabajo automáticamente.
"""
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.maintenance.models import MaintenancePlan, WorkOrder, MaintenanceTask
from app.maintenance.repository import MaintenanceRepository

# Logger específico para el scheduler
logger = logging.getLogger(__name__)

class MaintenanceScheduler:
    """
    Evalúa y ejecuta los planes de mantenimiento preventivo.
    """
    def __init__(self, db: Session):
        self.db = db
        self.repo = MaintenanceRepository(db)

    def run_preventive_maintenance_check(self):
        """
        Revisa todos los planes activos y genera órdenes si corresponde.
        Esta función debe ser llamada periódicamente.
        """
        logger.info("Iniciando chequeo de Mantenimiento Preventivo...")
        
        try:
            plans = self.db.query(MaintenancePlan).filter(MaintenancePlan.is_active == True).all()
            logger.info(f"Se encontraron {len(plans)} planes de mantenimiento activos para evaluar.")
            generated_count = 0
            
            for plan in plans:
                if self._should_execute_plan(plan):
                    try:
                        self._generate_order_from_plan(plan)
                        generated_count += 1
                    except Exception as e:
                        logger.error(f"Error generando orden para el plan '{plan.name}' (ID: {plan.id}): {e}", exc_info=True)
            
            logger.info(f"Chequeo de Mantenimiento Preventivo finalizado. {generated_count} órdenes generadas.")
        except Exception as e:
            logger.error(f"Error crítico durante la ejecución del scheduler: {e}", exc_info=True)

    def _should_execute_plan(self, plan: MaintenancePlan) -> bool:
        """Determina si un plan debe ejecutarse ahora basado en su intervalo."""
        if plan.trigger_type != "TIME_BASED":
            return False
            
        if not plan.last_execution_at:
            logger.debug(f"Plan '{plan.name}' nunca se ha ejecutado. Ejecutando ahora.")
            return True
            
        next_due_date = plan.last_execution_at + timedelta(days=plan.interval_days)
        now = datetime.now(timezone.utc)
        
        should_run = now >= next_due_date
        if should_run:
            logger.debug(f"Plan '{plan.name}' debe ejecutarse. Próxima fecha: {next_due_date}, Ahora: {now}")
        
        return should_run

    def _generate_order_from_plan(self, plan: MaintenancePlan):
        """Crea la WorkOrder y sus tareas basadas en la plantilla del plan."""
        logger.info(f"Ejecutando Plan de Mantenimiento: '{plan.name}'")
        
        # 1. Crear la Orden
        new_order = WorkOrder(
            asset_id=plan.asset_id,
            summary=plan.summary_template,
            description=f"Generado automáticamente por el plan: {plan.name}\n{plan.description or ''}",
            priority=plan.priority,
            category=plan.category,
            source_trigger={"type": "MAINTENANCE_PLAN", "plan_id": str(plan.id)},
            status="OPEN"
        )
        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)
        
        # 2. Copiar las Tareas
        logger.info(f"Copiando {len(plan.tasks)} tareas de la plantilla a la nueva orden {new_order.id}")
        for plan_task in plan.tasks:
            new_task = MaintenanceTask(
                work_order_id=new_order.id,
                description=plan_task.description,
                order=plan_task.order,
                is_completed=False
            )
            self.db.add(new_task)
            
        # 3. Actualizar el Plan
        plan.last_execution_at = datetime.now(timezone.utc)
        self.db.add(plan)
        
        self.db.commit()
        logger.info(f"Orden de Trabajo {new_order.id} generada exitosamente desde el plan '{plan.name}'.")
