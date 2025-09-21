# /app/maintenance/repository.py
"""
Capa de Repositorio para el módulo de Mantenimiento.

Encapsula la lógica de acceso a datos para las entidades WorkOrder,
MaintenanceTask y sus asignaciones.
"""

from typing import List, Optional
import uuid

from sqlalchemy.orm import Session, joinedload

from app.maintenance import models, schemas


class MaintenanceRepository:
    """Realiza operaciones CRUD en la base de datos para el módulo de Mantenimiento."""

    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para WorkOrder ---

    def create_work_order(self, work_order_in: schemas.WorkOrderCreate) -> models.WorkOrder:
        """Crea una nueva orden de trabajo en la base de datos."""
        db_work_order = models.WorkOrder(**work_order_in.model_dump())
        self.db.add(db_work_order)
        self.db.commit()
        self.db.refresh(db_work_order)
        return db_work_order

    def get_work_order(self, work_order_id: uuid.UUID) -> Optional[models.WorkOrder]:
        """Obtiene una orden de trabajo por su ID, cargando sus relaciones."""
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
        """Lista todas las órdenes de trabajo con paginación."""
        return self.db.query(models.WorkOrder).offset(skip).limit(limit).all()

    # --- Métodos para Asignaciones ---

    def assign_user_to_work_order(self, assignment_in: schemas.WorkOrderUserAssignmentCreate) -> models.WorkOrderUserAssignment:
        """Asigna un usuario a una orden de trabajo."""
        db_assignment = models.WorkOrderUserAssignment(**assignment_in.model_dump())
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_assignment)
        return db_assignment

    def assign_provider_to_work_order(self, assignment_in: schemas.WorkOrderProviderAssignmentCreate) -> models.WorkOrderProviderAssignment:
        """Asigna un proveedor a una orden de trabajo."""
        db_assignment = models.WorkOrderProviderAssignment(**assignment_in.model_dump())
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_assignment)
        return db_assignment
