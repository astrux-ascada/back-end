# /app/maintenance/service.py
"""
Capa de Servicio para el módulo de Mantenimiento.

Gestiona la lógica de negocio para Órdenes de Trabajo, Tareas, Planes y Asignaciones.
Coordina la interacción con el módulo de Compras para la gestión de inventario.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
import logging
from fastapi import HTTPException, status

from app.maintenance import schemas
from app.maintenance.models import WorkOrder, MaintenanceTask, MaintenancePlan
from app.maintenance.repository import MaintenanceRepository
from app.assets.repository import AssetRepository
from app.identity.repository import UserRepository
from app.procurement.repository import ProcurementRepository
from app.assets.mappers import map_asset_to_dto
from app.auditing.service import AuditService
from app.identity.models import User

# Configuración del logger para este módulo
logger = logging.getLogger(__name__)

class MaintenanceService:
    """
    Servicio principal para la gestión de mantenimiento.
    """

    def __init__(self, db: Session, audit_service: AuditService):
        self.db = db
        self.audit_service = audit_service
        self.repo = MaintenanceRepository(db)
        self.procurement_repo = ProcurementRepo(db)

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
        
        task = self.repo.create_task(order_id, task_in)
        logger.info(f"Tarea añadida a orden {order_id}: {task.description}")
        
        self.audit_service.log_operation(
            user=current_user, 
            action="ADD_TASK", 
            entity_type="MaintenanceTask", 
            entity_id=task.id, 
            details={"work_order_id": str(order_id), "description": task.description}
        )
        return task

        updated_work_order = self.maintenance_repo.update_work_order_status(work_order_id, tenant_id, new_status)
        
        updated_task = self.repo.update_task(task, task_in)
        logger.info(f"Tarea {task_id} actualizada. Completada: {updated_task.is_completed}")
        
        self.audit_service.log_operation(
            user=current_user, 
            action="UPDATE_TASK", 
            entity_type="MaintenanceTask", 
            entity_id=task.id, 
            details=task_in.model_dump(exclude_unset=True)
        )
        return updated_task

    # --- User Assignments ---

    def assign_user_to_order(self, order_id: UUID, user_id: UUID, current_user: User) -> bool:
        """Asigna un técnico a una orden."""
        if not self.repo.get(order_id): 
            return False
        
        success = self.repo.assign_user(order_id, user_id)
        if success:
            logger.info(f"Usuario {user_id} asignado a orden {order_id}")
            self.audit_service.log_operation(
                user=current_user, 
                action="ASSIGN_USER", 
                entity_type="WorkOrder", 
                entity_id=order_id, 
                details={"assigned_user_id": str(user_id)}
            )
        return success

    def unassign_user_from_order(self, order_id: UUID, user_id: UUID, current_user: User) -> bool:
        """Desasigna un técnico de una orden."""
        if not self.repo.get(order_id): 
            return False
        
        success = self.repo.unassign_user(order_id, user_id)
        if success:
            logger.info(f"Usuario {user_id} desasignado de orden {order_id}")
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
        
        self.repo.add_spare_part_to_order(order_id, request.spare_part_id, request.quantity_required)
        logger.info(f"Repuesto '{part.name}' (x{request.quantity_required}) añadido a orden {order_id}")
        
        self.audit_service.log_operation(
            user=user,
            action="ASSIGN_USER_TO_WORK_ORDER",
            entity=work_order,
            details={"assigned_user_id": str(user_to_assign.id), "assigned_user_email": user_to_assign.email}
        )
        return self.repo.get(order_id)

    def remove_spare_part_from_order(self, order_id: UUID, part_id: UUID, current_user: User) -> Optional[WorkOrder]:
        """Desvincula un repuesto de una orden."""
        order = self.repo.get(order_id)
        if not order:
            return None
        
        success = self.repo.remove_spare_part_from_order(order_id, part_id)
        if success:
            logger.info(f"Repuesto {part_id} removido de orden {order_id}")
            self.audit_service.log_operation(
                user=current_user, 
                action="REMOVE_SPARE_PART", 
                entity_type="WorkOrder", 
                entity_id=order_id, 
                details={"spare_part_id": str(part_id)}
            )
        
        return self.repo.get(order_id)

    # --- Maintenance Plans ---

    def create_plan(self, plan_in: schemas.MaintenancePlanCreate, current_user: User) -> MaintenancePlan:
        """Crea un nuevo Plan de Mantenimiento Preventivo."""
        logger.info(f"Creando Plan de Mantenimiento: '{plan_in.name}'")
        plan = MaintenancePlan(**plan_in.model_dump(exclude={"tasks"}))
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        
        for task_data in plan_in.tasks:
            # Nota: Idealmente esto iría en el repo, pero por brevedad lo mantenemos aquí
            from app.maintenance.models import MaintenancePlanTask
            task = MaintenancePlanTask(plan_id=plan.id, **task_data.model_dump())
            self.db.add(task)
            
        self.db.commit()
        self.db.refresh(plan)
        logger.info(f"Plan de Mantenimiento creado. ID: {plan.id}")
        return plan

    def list_plans(self, skip: int = 0, limit: int = 100) -> List[MaintenancePlan]:
        """Lista los planes de mantenimiento."""
        return self.db.query(MaintenancePlan).offset(skip).limit(limit).all()
