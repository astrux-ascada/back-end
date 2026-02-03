# /app/maintenance/repository.py
"""
Capa de Repositorio para el módulo de Mantenimiento.
"""
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session, joinedload

from app.maintenance import models, schemas
from app.assets.models import Asset # Importar Asset para el join

class MaintenanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_work_order(self, work_order_in: schemas.WorkOrderCreate, tenant_id: uuid.UUID) -> models.WorkOrder:
        db_work_order = models.WorkOrder(**work_order_in.model_dump(), tenant_id=tenant_id)
        self.db.add(db_work_order)
        self.db.commit()
        self.db.refresh(db_work_order)
        return db_work_order

    def get_work_order(self, work_order_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.WorkOrder]:
        return (
            self.db.query(models.WorkOrder)
            .options(
                joinedload(models.WorkOrder.asset).joinedload(Asset.asset_type),
                joinedload(models.WorkOrder.tasks),
                joinedload(models.WorkOrder.assigned_users),
                joinedload(models.WorkOrder.assigned_provider),
            )
            .filter(models.WorkOrder.id == work_order_id, models.WorkOrder.tenant_id == tenant_id) # Filtro por tenant
            .first()
        )

    def list_work_orders(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.WorkOrder]:
        return (
            self.db.query(models.WorkOrder)
            .filter(models.WorkOrder.tenant_id == tenant_id) # Filtro por tenant
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_work_order_status(self, work_order_id: uuid.UUID, tenant_id: uuid.UUID, new_status: str) -> Optional[models.WorkOrder]:
        """Actualiza el campo de estado de una orden de trabajo específica."""
        db_work_order = self.get_work_order(work_order_id, tenant_id) # Reutilizamos para asegurar pertenencia
        if db_work_order:
            db_work_order.status = new_status
            self.db.commit()
            self.db.refresh(db_work_order)
        return db_work_order

    def assign_user_to_work_order(self, assignment_in: schemas.WorkOrderUserAssignmentCreate) -> models.WorkOrderUserAssignment:
        # Aquí necesitaríamos validar que tanto la WorkOrder como el User pertenecen al mismo tenant
        db_assignment = models.WorkOrderUserAssignment(**assignment_in.model_dump())
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_task(self, task_id: UUID) -> Optional[MaintenanceTask]:
        return self.db.query(MaintenanceTask).filter(MaintenanceTask.id == task_id).first()

    def assign_provider_to_work_order(self, assignment_in: schemas.WorkOrderProviderAssignmentCreate) -> models.WorkOrderProviderAssignment:
        # Aquí necesitaríamos validar que tanto la WorkOrder como el Provider pertenecen al mismo tenant
        db_assignment = models.WorkOrderProviderAssignment(**assignment_in.model_dump())
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task
    
    def delete_task(self, task_id: UUID) -> bool:
        db_task = self.get_task(task_id)
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
            return True
        return False

    # --- User Assignments ---

    def assign_user(self, work_order_id: UUID, user_id: UUID) -> bool:
        exists = self.db.query(WorkOrderUserAssignment).filter_by(work_order_id=work_order_id, user_id=user_id).first()
        if not exists:
            assignment = WorkOrderUserAssignment(work_order_id=work_order_id, user_id=user_id)
            self.db.add(assignment)
            self.db.commit()
            return True
        return False

    def unassign_user(self, work_order_id: UUID, user_id: UUID) -> bool:
        assignment = self.db.query(WorkOrderUserAssignment).filter_by(work_order_id=work_order_id, user_id=user_id).first()
        if assignment:
            self.db.delete(assignment)
            self.db.commit()
            return True
        return False

    # --- Spare Part Assignments ---

    def add_spare_part_to_order(self, order_id: UUID, part_id: UUID, quantity: int) -> Optional[WorkOrderSparePart]:
        """Asigna un repuesto a una orden o actualiza la cantidad si ya existe."""
        assignment = self.db.query(WorkOrderSparePart).filter_by(work_order_id=order_id, spare_part_id=part_id).first()
        if assignment:
            assignment.quantity_required = quantity
        else:
            assignment = WorkOrderSparePart(work_order_id=order_id, spare_part_id=part_id, quantity_required=quantity)
        
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def remove_spare_part_from_order(self, order_id: UUID, part_id: UUID) -> bool:
        """Quita un repuesto de una orden."""
        assignment = self.db.query(WorkOrderSparePart).filter_by(work_order_id=order_id, spare_part_id=part_id).first()
        if assignment:
            self.db.delete(assignment)
            self.db.commit()
            return True
        return False
