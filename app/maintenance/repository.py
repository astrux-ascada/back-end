# /app/maintenance/repository.py
"""
Capa de Repositorio para el módulo de Mantenimiento.
"""
from typing import List, Optional
import uuid
from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.maintenance import models, schemas
from app.maintenance.models.work_order_provider_assignment import WorkOrderProviderAssignment

class MaintenanceRepository:
    """Realiza operaciones CRUD para las órdenes de trabajo."""

    def __init__(self, db: Session):
        self.db = db

    def create_work_order(self, work_order_in: schemas.WorkOrderCreate, tenant_id: uuid.UUID) -> models.WorkOrder:
        db_work_order = models.WorkOrder(**work_order_in.model_dump(), tenant_id=tenant_id)
        self.db.add(db_work_order)
        self.db.commit()
        self.db.refresh(db_work_order)
        return db_work_order

    def get_work_order(self, work_order_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.WorkOrder]:
        return self.db.query(models.WorkOrder).filter(
            models.WorkOrder.id == work_order_id,
            models.WorkOrder.tenant_id == tenant_id
        ).first()

    def list_work_orders(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.WorkOrder]:
        return self.db.query(models.WorkOrder).filter(
            models.WorkOrder.tenant_id == tenant_id
        ).offset(skip).limit(limit).all()

    def update_work_order(self, db_work_order: models.WorkOrder, work_order_in: schemas.WorkOrderUpdate) -> models.WorkOrder:
        update_data = work_order_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_work_order, field, value)
        self.db.add(db_work_order)
        self.db.commit()
        self.db.refresh(db_work_order)
        return db_work_order

    def cancel_work_order(self, db_work_order: models.WorkOrder, reason: str) -> models.WorkOrder:
        db_work_order.status = "CANCELLED"
        db_work_order.cancellation_reason = reason
        self.db.add(db_work_order)
        self.db.commit()
        self.db.refresh(db_work_order)
        return db_work_order

    def assign_provider(self, work_order_id: uuid.UUID, provider_id: uuid.UUID, notes: Optional[str], estimated_cost: Optional[float]) -> WorkOrderProviderAssignment:
        assignment = WorkOrderProviderAssignment(
            work_order_id=work_order_id,
            provider_id=provider_id,
            notes=notes,
            estimated_cost=estimated_cost
        )
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def update_evaluation(self, db_work_order: models.WorkOrder, rating: int, feedback: Optional[str]) -> models.WorkOrder:
        db_work_order.rating = rating
        db_work_order.feedback = feedback
        self.db.add(db_work_order)
        self.db.commit()
        self.db.refresh(db_work_order)
        return db_work_order
