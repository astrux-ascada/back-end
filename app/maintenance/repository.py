# /app/maintenance/repository.py
"""
Capa de Repositorio para el módulo de Mantenimiento.
"""

from typing import List, Optional
import uuid

from sqlalchemy.orm import Session, joinedload

from app.maintenance import models, schemas


class MaintenanceRepository:
    """Realiza operaciones CRUD en la base de datos para el módulo de Mantenimiento."""

    def __init__(self, db: Session):
        self.db = db

    def create_work_order(self, work_order_in: schemas.WorkOrderCreate) -> models.WorkOrder:
        db_work_order = models.WorkOrder(**work_order_in.model_dump())
        self.db.add(db_work_order)
        self.db.commit()
        self.db.refresh(db_work_order)
        return db_work_order

    def get_work_order(self, work_order_id: uuid.UUID) -> Optional[models.WorkOrder]:
        return (
            self.db.query(models.WorkOrder)
            .options(
                joinedload(models.WorkOrder.asset).joinedload(models.Asset.asset_type),
                joinedload(models.WorkOrder.tasks),
                joinedload(models.WorkOrder.assigned_users),
                joinedload(models.WorkOrder.assigned_provider),
            )
            .filter(models.WorkOrder.id == work_order_id)
            .first()
        )

    def list_work_orders(self, skip: int = 0, limit: int = 100) -> List[models.WorkOrder]:
        return self.db.query(models.WorkOrder).offset(skip).limit(limit).all()

    def update_work_order_status(self, work_order_id: uuid.UUID, new_status: str) -> Optional[models.WorkOrder]:
        """Actualiza el campo de estado de una orden de trabajo específica."""
        db_work_order = self.get_work_order(work_order_id)
        if db_work_order:
            db_work_order.status = new_status
            self.db.commit()
            self.db.refresh(db_work_order)
        return db_work_order

    def assign_user_to_work_order(self, assignment_in: schemas.WorkOrderUserAssignmentCreate) -> models.WorkOrderUserAssignment:
        db_assignment = models.WorkOrderUserAssignment(**assignment_in.model_dump())
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_assignment)
        return db_assignment

    def assign_provider_to_work_order(self, assignment_in: schemas.WorkOrderProviderAssignmentCreate) -> models.WorkOrderProviderAssignment:
        db_assignment = models.WorkOrderProviderAssignment(**assignment_in.model_dump())
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_assignment)
        return db_assignment
