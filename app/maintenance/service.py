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
from app.procurement.repository import ProcurementRepository as ProcurementRepo
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

    # --- Work Orders ---

    def create_order(self, order_in: schemas.WorkOrderCreate, current_user: Optional[User] = None) -> WorkOrder:
        """
        Crea una nueva Orden de Trabajo.
        
        Args:
            order_in: Datos de la orden.
            current_user: Usuario que realiza la acción (puede ser None si es sistema).
        """
        logger.info(f"Creando nueva Orden de Trabajo. Resumen: '{order_in.summary}', Prioridad: {order_in.priority}")
        order = self.repo.create(order_in)
        
        self.audit_service.log_operation(
            user=current_user, 
            action="CREATE_WORK_ORDER", 
            entity_type="WorkOrder", 
            entity_id=order.id, 
            details={"summary": order.summary, "priority": order.priority}
        )
        logger.info(f"Orden de Trabajo creada exitosamente. ID: {order.id}")
        return order

    def get_order(self, order_id: UUID) -> Optional[WorkOrder]:
        """Obtiene una orden por su ID."""
        return self.repo.get(order_id)

    def list_orders(self, skip: int = 0, limit: int = 100, status: str = None, asset_id: UUID = None) -> List[WorkOrder]:
        """Lista órdenes con filtros opcionales."""
        return self.repo.get_multi(skip, limit, status, asset_id)

    def update_order(self, order_id: UUID, order_in: schemas.WorkOrderUpdate, current_user: User) -> Optional[WorkOrder]:
        """
        Actualiza una orden existente. Maneja la validación y descuento de stock al completar.
        """
        logger.info(f"Actualizando Orden de Trabajo {order_id}. Datos: {order_in.model_dump(exclude_unset=True)}")
        order = self.repo.get(order_id)
        if not order:
            logger.warning(f"Intento de actualizar orden inexistente: {order_id}")
            return None
        
        old_status = order.status
        
        # Validar stock antes de completar
        if order_in.status == "COMPLETED" and old_status != "COMPLETED":
            logger.info(f"Validando stock para completar la orden {order_id}...")
            self._validate_stock_for_completion(order)

        updated_order = self.repo.update(order, order_in)
        
        # Descontar stock después de completar
        if updated_order.status == "COMPLETED" and old_status != "COMPLETED":
            self._deduct_stock_for_order(updated_order)

        self.audit_service.log_operation(
            user=current_user, 
            action="UPDATE_WORK_ORDER", 
            entity_type="WorkOrder", 
            entity_id=order.id, 
            details=order_in.model_dump(exclude_unset=True)
        )
        return updated_order

    def _validate_stock_for_completion(self, order: WorkOrder):
        """
        Verifica si hay stock suficiente para todos los repuestos requeridos.
        Lanza HTTPException 409 si no hay stock.
        """
        for item in order.required_spare_parts:
            part = self.procurement_repo.get_spare_part(item.spare_part_id)
            if not part or part.current_stock < item.quantity_required:
                error_msg = f"Stock insuficiente. Repuesto: '{part.name if part else 'Desconocido'}'. Req: {item.quantity_required}, Disp: {part.current_stock if part else 'N/A'}"
                logger.error(f"Error de validación de stock en orden {order.id}: {error_msg}")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=error_msg
                )

    def _deduct_stock_for_order(self, order: WorkOrder):
        """Descuenta del inventario los repuestos usados."""
        logger.info(f"Iniciando descuento de stock para orden {order.id}")
        for item in order.required_spare_parts:
            part = self.procurement_repo.get_spare_part(item.spare_part_id)
            if part:
                old_stock = part.current_stock
                new_stock = old_stock - item.quantity_required
                self.procurement_repo.update_spare_part(part, schemas.SparePartUpdate(current_stock=new_stock))
                logger.info(f"Stock actualizado para '{part.name}': {old_stock} -> {new_stock}")

    # --- Maintenance Tasks ---

    def add_task_to_order(self, order_id: UUID, task_in: schemas.MaintenanceTaskCreate, current_user: User) -> Optional[MaintenanceTask]:
        """Añade una tarea a una orden."""
        if not self.repo.get(order_id): 
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

    def update_task(self, task_id: UUID, task_in: schemas.MaintenanceTaskUpdate, current_user: User) -> Optional[MaintenanceTask]:
        """Actualiza una tarea (ej: marcar como completada)."""
        task = self.repo.get_task(task_id)
        if not task: 
            return None
        
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
                user=current_user, 
                action="UNASSIGN_USER", 
                entity_type="WorkOrder", 
                entity_id=order_id, 
                details={"unassigned_user_id": str(user_id)}
            )
        return success

    # --- Spare Part Assignments ---

    def add_spare_part_to_order(self, order_id: UUID, request: schemas.AddSparePartRequest, current_user: User) -> Optional[WorkOrder]:
        """Vincula un repuesto a una orden."""
        order = self.repo.get(order_id)
        part = self.procurement_repo.get_spare_part(request.spare_part_id)
        if not order or not part:
            logger.warning(f"Fallo al añadir repuesto. Orden {order_id} o Parte {request.spare_part_id} no encontrados.")
            return None
        
        self.repo.add_spare_part_to_order(order_id, request.spare_part_id, request.quantity_required)
        logger.info(f"Repuesto '{part.name}' (x{request.quantity_required}) añadido a orden {order_id}")
        
        self.audit_service.log_operation(
            user=current_user, 
            action="ADD_SPARE_PART", 
            entity_type="WorkOrder", 
            entity_id=order_id, 
            details={"spare_part_id": str(request.spare_part_id), "quantity": request.quantity_required}
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
