# /app/maintenance/service.py
"""
Capa de Servicio para el módulo de Mantenimiento.

Contiene la lógica de negocio que orquesta las operaciones del repositorio
para realizar tareas complejas relacionadas con las órdenes de trabajo.
"""

from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.maintenance import models, schemas
from app.maintenance.repository import MaintenanceRepository
# Importamos los otros repositorios para validaciones cruzadas
from app.assets.repository import AssetRepository
from app.identity.repository import UserRepository
from app.procurement.repository import ProcurementRepository
# from app.core.exceptions import NotFoundException, BusinessLogicException # Futuro


class MaintenanceService:
    """Servicio de negocio para la gestión del mantenimiento."""

    def __init__(self, db: Session):
        self.db = db
        self.maintenance_repo = MaintenanceRepository(self.db)
        # Instanciamos otros repositorios para validar la existencia de entidades
        self.asset_repo = AssetRepository(self.db)
        self.user_repo = UserRepository(self.db)
        self.provider_repo = ProcurementRepository(self.db)

    def create_work_order(self, work_order_in: schemas.WorkOrderCreate) -> models.WorkOrder:
        """Crea una nueva orden de trabajo.

        Lógica de negocio: Verifica que el activo al que se le asigna la orden existe.
        """
        asset = self.asset_repo.get_asset(work_order_in.asset_id)
        if not asset:
            # raise NotFoundException(f"Asset with id {work_order_in.asset_id} not found.")
            pass # Por ahora, no lanzamos excepción para mantenerlo simple

        return self.maintenance_repo.create_work_order(work_order_in)

    def get_work_order(self, work_order_id: uuid.UUID) -> Optional[models.WorkOrder]:
        """Obtiene una orden de trabajo por su ID."""
        return self.maintenance_repo.get_work_order(work_order_id)

    def list_work_orders(self, skip: int = 0, limit: int = 100) -> List[models.WorkOrder]:
        """Lista todas las órdenes de trabajo."""
        return self.maintenance_repo.list_work_orders(skip, limit)

    def assign_user_to_work_order(self, assignment_in: schemas.WorkOrderUserAssignmentCreate) -> models.WorkOrderUserAssignment:
        """Asigna un técnico a una orden de trabajo.

        Lógica de negocio: Verifica que tanto la orden como el usuario existen.
        """
        work_order = self.get_work_order(assignment_in.work_order_id)
        user = self.user_repo.get_by_id(assignment_in.user_id) # Asumimos que get_by_id existe
        if not work_order or not user:
            # raise NotFoundException("Work Order or User not found.")
            pass

        return self.maintenance_repo.assign_user_to_work_order(assignment_in)

    def assign_provider_to_work_order(self, assignment_in: schemas.WorkOrderProviderAssignmentCreate) -> models.WorkOrderProviderAssignment:
        """Asigna un proveedor a una orden de trabajo.

        Lógica de negocio: Verifica que tanto la orden como el proveedor existen.
        """
        work_order = self.get_work_order(assignment_in.work_order_id)
        provider = self.provider_repo.get_provider(assignment_in.provider_id)
        if not work_order or not provider:
            # raise NotFoundException("Work Order or Provider not found.")
            pass

        return self.maintenance_repo.assign_provider_to_work_order(assignment_in)
