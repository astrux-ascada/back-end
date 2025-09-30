# /app/maintenance/service.py
"""
Capa de Servicio para el módulo de Mantenimiento.

Contiene la lógica de negocio que orquesta las operaciones del repositorio
y transforma los modelos de la base de datos en los DTOs para la API.
"""

from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.maintenance import models, schemas
from app.maintenance.repository import MaintenanceRepository
# --- MEJORA: Importar dependencias para validación y mapeo ---
from app.assets.repository import AssetRepository
from app.identity.repository import UserRepository
from app.procurement.repository import ProcurementRepository
from app.assets.mappers import map_asset_to_dto


class MaintenanceService:
    """Servicio de negocio para la gestión del mantenimiento."""

    def __init__(self, db: Session):
        self.db = db
        self.maintenance_repo = MaintenanceRepository(self.db)
        self.asset_repo = AssetRepository(self.db)
        self.user_repo = UserRepository(self.db)
        self.provider_repo = ProcurementRepository(self.db)

    def create_work_order(self, work_order_in: schemas.WorkOrderCreate) -> schemas.WorkOrderRead:
        """Crea una nueva orden de trabajo y la devuelve como DTO."""
        # Lógica de negocio: Validar que el activo existe
        asset = self.asset_repo.get_asset(work_order_in.asset_id)
        if not asset:
            raise ValueError(f"Asset with id {work_order_in.asset_id} not found.")

        db_work_order = self.maintenance_repo.create_work_order(work_order_in)
        # Volvemos a cargar la orden para obtener todas las relaciones pobladas
        full_work_order = self.maintenance_repo.get_work_order(db_work_order.id)
        return self.get_work_order(full_work_order.id) # Reutilizamos el método que ya mapea

    def get_work_order(self, work_order_id: uuid.UUID) -> Optional[schemas.WorkOrderRead]:
        """Obtiene una orden de trabajo por su ID y la mapea a un DTO."""
        work_order = self.maintenance_repo.get_work_order(work_order_id)
        if not work_order:
            return None

        # --- MEJORA: Mapear el Asset anidado al DTO correcto ---
        asset_dto = map_asset_to_dto(work_order.asset, self.asset_repo)

        # Construir el DTO final de WorkOrderRead
        return schemas.WorkOrderRead(
            **work_order.__dict__,
            asset=asset_dto
        )

    def list_work_orders(self, skip: int = 0, limit: int = 100) -> List[schemas.WorkOrderRead]:
        """Lista órdenes de trabajo y las mapea a una lista de DTOs."""
        work_orders = self.maintenance_repo.list_work_orders(skip, limit)
        # Mapeamos cada orden de trabajo individualmente para construir el DTO completo
        return [self.get_work_order(wo.id) for wo in work_orders if self.get_work_order(wo.id) is not None]

    def assign_user_to_work_order(self, assignment_in: schemas.WorkOrderUserAssignmentCreate) -> models.WorkOrderUserAssignment:
        work_order = self.maintenance_repo.get_work_order(assignment_in.work_order_id)
        user = self.user_repo.get_by_id(assignment_in.user_id)
        if not work_order or not user:
            raise ValueError("Work Order or User not found.")
        return self.maintenance_repo.assign_user_to_work_order(assignment_in)

    def assign_provider_to_work_order(self, assignment_in: schemas.WorkOrderProviderAssignmentCreate) -> models.WorkOrderProviderAssignment:
        work_order = self.maintenance_repo.get_work_order(assignment_in.work_order_id)
        provider = self.provider_repo.get_provider(assignment_in.provider_id)
        if not work_order or not provider:
            raise ValueError("Work Order or Provider not found.")
        return self.maintenance_repo.assign_provider_to_work_order(assignment_in)
