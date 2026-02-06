# /app/db/seeding/_seed_maintenance.py
"""
Seeder para el módulo de Mantenimiento (Órdenes de Trabajo).
"""
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.maintenance.models.work_order import WorkOrder, WorkOrderStatus, WorkOrderPriority

logger = logging.getLogger(__name__)

async def seed_maintenance(db: Session, context: dict):
    logger.info("--- [6/9] Poblando Mantenimiento (Órdenes de Trabajo) ---")
    
    demo_tenant = context["demo_tenant"]
    brazo_robotico = context["brazo_robotico"]

    # Crear una Orden de Trabajo Correctiva
    wo = db.query(WorkOrder).filter(WorkOrder.title == "Reemplazo de rodamiento eje 3", WorkOrder.tenant_id == demo_tenant.id).first()
    if not wo:
        wo = WorkOrder(
            tenant_id=demo_tenant.id,
            asset_id=brazo_robotico.id,
            title="Reemplazo de rodamiento eje 3",
            description="El rodamiento del eje 3 presenta vibraciones anormales.",
            priority=WorkOrderPriority.HIGH,
            category="CORRECTIVE",
            status=WorkOrderStatus.OPEN,
            due_date=datetime.utcnow() + timedelta(days=2)
        )
        db.add(wo)
        db.commit()
