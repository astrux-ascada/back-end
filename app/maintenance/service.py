# /app/maintenance/service.py
"""
Capa de Servicio para el módulo de Mantenimiento.
"""

from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.maintenance import models, schemas
from app.maintenance.repository import MaintenanceRepository
from app.assets.repository import AssetRepository
from app.identity.repository import UserRepository
from app.procurement.repository import ProcurementRepository
from app.assets.mappers import map_asset_to_dto
from app.auditing.service import AuditService
from app.identity.models import User


class MaintenanceService:
    """Servicio de negocio para la gestión del mantenimiento."""

    def __init__(self, db: Session, audit_service: AuditService):
        self.db = db
        self.audit_service = audit_service
        self.maintenance_repo = MaintenanceRepository(self.db)
        self.asset_repo = AssetRepository(self.db)
        self.user_repo = UserRepository(self.db)
        self.provider_repo = ProcurementRepository(self.db)

    def create_work_order(self, work_order_in: schemas.WorkOrderCreate, user: User, tenant_id: uuid.UUID) -> schemas.WorkOrderRead:
        """Crea una nueva orden de trabajo y registra la acción."""
        # Validar que el activo pertenece al tenant
        asset = self.asset_repo.get_asset(work_order_in.asset_id, tenant_id)
        if not asset:
            raise ValueError(f"Asset with id {work_order_in.asset_id} not found in this tenant.")

        db_work_order = self.maintenance_repo.create_work_order(work_order_in, tenant_id)
        
        self.audit_service.log_operation(
            user=user,
            action="CREATE_WORK_ORDER",
            entity=db_work_order
        )
        
        return self.get_work_order(db_work_order.id, tenant_id)

    def get_work_order(self, work_order_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[schemas.WorkOrderRead]:
        work_order = self.maintenance_repo.get_work_order(work_order_id, tenant_id)
        if not work_order:
            return None
        # El asset ya viene filtrado por tenant desde el repo de mantenimiento
        asset_dto = map_asset_to_dto(work_order.asset, self.asset_repo)
        return schemas.WorkOrderRead(**work_order.__dict__, asset=asset_dto)

    def list_work_orders(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[schemas.WorkOrderRead]:
        work_orders = self.maintenance_repo.list_work_orders(tenant_id, skip, limit)
        # Optimizacion: Evitar N+1 queries llamando a get_work_order repetidamente
        return [
            schemas.WorkOrderRead(**wo.__dict__, asset=map_asset_to_dto(wo.asset, self.asset_repo))
            for wo in work_orders
        ]

    def update_work_order_status(self, work_order_id: uuid.UUID, status_update: schemas.WorkOrderStatusUpdate, user: User, tenant_id: uuid.UUID) -> Optional[schemas.WorkOrderRead]:
        """Actualiza el estado de una orden de trabajo y registra la acción."""
        work_order_before_update = self.maintenance_repo.get_work_order(work_order_id, tenant_id)
        if not work_order_before_update:
            return None
        
        old_status = work_order_before_update.status
        new_status = status_update.status

        updated_work_order = self.maintenance_repo.update_work_order_status(work_order_id, tenant_id, new_status)
        
        if updated_work_order:
            self.audit_service.log_operation(
                user=user,
                action="UPDATE_WORK_ORDER_STATUS",
                entity=updated_work_order,
                details={"from": old_status, "to": new_status}
            )
            return self.get_work_order(updated_work_order.id, tenant_id)
        return None

    def assign_user_to_work_order(self, assignment_in: schemas.WorkOrderUserAssignmentCreate, user: User, tenant_id: uuid.UUID) -> models.WorkOrderUserAssignment:
        work_order = self.maintenance_repo.get_work_order(assignment_in.work_order_id, tenant_id)
        # Validar que el usuario a asignar pertenece al mismo tenant
        user_to_assign = self.user_repo.get_by_id_and_tenant(assignment_in.user_id, tenant_id)
        if not work_order or not user_to_assign:
            raise ValueError("Work Order or User not found in this tenant.")
        
        assignment = self.maintenance_repo.assign_user_to_work_order(assignment_in)
        
        self.audit_service.log_operation(
            user=user,
            action="ASSIGN_USER_TO_WORK_ORDER",
            entity=work_order,
            details={"assigned_user_id": str(user_to_assign.id), "assigned_user_email": user_to_assign.email}
        )
        return assignment
