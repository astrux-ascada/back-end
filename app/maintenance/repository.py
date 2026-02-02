# /app/maintenance/repository.py
"""
Capa de Repositorio para el módulo de Mantenimiento.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.maintenance.models import WorkOrder, MaintenanceTask, WorkOrderUserAssignment, WorkOrderSparePart
from app.maintenance import schemas
from app.identity.models import User

class MaintenanceRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- Work Orders ---

    def create(self, order_in: schemas.WorkOrderCreate) -> WorkOrder:
        order_data = order_in.model_dump(exclude={"tasks", "assigned_user_ids"})
        db_order = WorkOrder(**order_data)
        
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)

        if order_in.tasks:
            for task_in in order_in.tasks:
                db_task = MaintenanceTask(work_order_id=db_order.id, **task_in.model_dump())
                self.db.add(db_task)
        
        if order_in.assigned_user_ids:
            for user_id in order_in.assigned_user_ids:
                assignment = WorkOrderUserAssignment(work_order_id=db_order.id, user_id=user_id)
                self.db.add(assignment)

        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def get(self, order_id: UUID) -> Optional[WorkOrder]:
        return self.db.query(WorkOrder).filter(WorkOrder.id == order_id).first()

    def get_multi(self, skip: int = 0, limit: int = 100, status: Optional[str] = None, asset_id: Optional[UUID] = None) -> List[WorkOrder]:
        query = self.db.query(WorkOrder)
        if status:
            query = query.filter(WorkOrder.status == status)
        if asset_id:
            query = query.filter(WorkOrder.asset_id == asset_id)
        return query.order_by(desc(WorkOrder.created_at)).offset(skip).limit(limit).all()

    def update(self, db_order: WorkOrder, order_in: schemas.WorkOrderUpdate) -> WorkOrder:
        update_data = order_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    # --- Maintenance Tasks ---

    def create_task(self, work_order_id: UUID, task_in: schemas.MaintenanceTaskCreate) -> MaintenanceTask:
        db_task = MaintenanceTask(work_order_id=work_order_id, **task_in.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_task(self, task_id: UUID) -> Optional[MaintenanceTask]:
        return self.db.query(MaintenanceTask).filter(MaintenanceTask.id == task_id).first()

    def update_task(self, db_task: MaintenanceTask, task_in: schemas.MaintenanceTaskUpdate) -> MaintenanceTask:
        update_data = task_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        self.db.add(db_task)
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
