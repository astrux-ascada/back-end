# /app/maintenance/service.py
"""
Capa de Servicio para el módulo de Mantenimiento.
"""
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.maintenance import models, schemas
from app.maintenance.repository import MaintenanceRepository
from app.procurement.repository import ProcurementRepository
from app.core.exceptions import NotFoundException, ConflictException
from app.auditing.service import AuditService
from app.identity.models import User

class MaintenanceService:
    """Servicio de negocio para la gestión de órdenes de trabajo."""

    def __init__(self, db: Session, audit_service: AuditService):
        self.db = db
        self.audit_service = audit_service
        self.maintenance_repo = MaintenanceRepository(self.db)
        self.procurement_repo = ProcurementRepository(self.db)

    def create_work_order(self, work_order_in: schemas.WorkOrderCreate, tenant_id: uuid.UUID, user: User) -> models.WorkOrder:
        work_order = self.maintenance_repo.create_work_order(work_order_in, tenant_id)
        self.audit_service.log_operation(user, "CREATE_WORK_ORDER", work_order)
        return work_order

    def get_work_order(self, work_order_id: uuid.UUID, tenant_id: uuid.UUID) -> models.WorkOrder:
        work_order = self.maintenance_repo.get_work_order(work_order_id, tenant_id)
        if not work_order:
            raise NotFoundException("Orden de trabajo no encontrada.")
        return work_order

    def list_work_orders(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.WorkOrder]:
        return self.maintenance_repo.list_work_orders(tenant_id, skip, limit)

    def update_work_order(self, work_order_id: uuid.UUID, work_order_in: schemas.WorkOrderUpdate, tenant_id: uuid.UUID, user: User) -> models.WorkOrder:
        db_work_order = self.get_work_order(work_order_id, tenant_id)
        updated_work_order = self.maintenance_repo.update_work_order(db_work_order, work_order_in)
        self.audit_service.log_operation(user, "UPDATE_WORK_ORDER", updated_work_order, details=work_order_in.model_dump(exclude_unset=True))
        return updated_work_order

    def cancel_work_order(self, work_order_id: uuid.UUID, cancel_in: schemas.WorkOrderCancel, tenant_id: uuid.UUID, user: User) -> models.WorkOrder:
        db_work_order = self.get_work_order(work_order_id, tenant_id)
        
        if db_work_order.status in ["COMPLETED", "CANCELLED"]:
            raise ConflictException(f"No se puede cancelar una orden en estado {db_work_order.status}.")
            
        cancelled_work_order = self.maintenance_repo.cancel_work_order(db_work_order, cancel_in.cancellation_reason)
        self.audit_service.log_operation(user, "CANCEL_WORK_ORDER", cancelled_work_order, details={"reason": cancel_in.cancellation_reason})
        return cancelled_work_order

    def assign_provider(self, work_order_id: uuid.UUID, assignment_in: schemas.WorkOrderProviderAssignment, tenant_id: uuid.UUID, user: User) -> models.WorkOrder:
        db_work_order = self.get_work_order(work_order_id, tenant_id)
        
        provider = self.procurement_repo.get_provider(assignment_in.provider_id, tenant_id)
        if not provider:
            raise NotFoundException(f"El proveedor con ID {assignment_in.provider_id} no existe.")

        self.maintenance_repo.assign_provider(
            work_order_id, 
            assignment_in.provider_id, 
            assignment_in.notes, 
            assignment_in.estimated_cost
        )
        
        self.audit_service.log_operation(user, "ASSIGN_PROVIDER_TO_WORK_ORDER", db_work_order, details={"provider_id": str(assignment_in.provider_id)})
        return db_work_order

    def evaluate_work_order(self, work_order_id: uuid.UUID, evaluation_in: schemas.WorkOrderEvaluation, tenant_id: uuid.UUID, user: User) -> models.WorkOrder:
        """
        Añade una calificación y feedback a una orden de trabajo completada.
        """
        db_work_order = self.get_work_order(work_order_id, tenant_id)

        if db_work_order.status != models.WorkOrderStatus.COMPLETED:
            raise ConflictException("Solo se pueden evaluar órdenes de trabajo completadas.")

        if db_work_order.rating is not None:
            raise ConflictException("Esta orden de trabajo ya ha sido evaluada.")

        # Actualizar el repositorio para guardar la evaluación
        evaluated_work_order = self.maintenance_repo.update_evaluation(db_work_order, evaluation_in.rating, evaluation_in.feedback)
        
        self.audit_service.log_operation(user, "EVALUATE_WORK_ORDER", evaluated_work_order, details=evaluation_in.model_dump())
        return evaluated_work_order
