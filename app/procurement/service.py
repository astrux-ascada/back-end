# /app/procurement/service.py
"""
Capa de Servicio para el módulo de Compras (Procurement).
"""

from typing import List, Optional
import uuid
import logging
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.procurement import models, schemas
from app.procurement.repository import ProcurementRepository

logger = logging.getLogger(__name__)

class ProcurementService:
    """
    Servicio principal para la gestión de compras.
    """
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProcurementRepository(self.db)

    # --- Métodos para Provider ---

    def create_provider(self, provider_in: schemas.ProviderCreate, tenant_id: uuid.UUID) -> models.Provider:
        return self.procurement_repo.create_provider(provider_in, tenant_id)

    def get_provider(self, provider_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.Provider]:
        return self.procurement_repo.get_provider(provider_id, tenant_id)

    def list_providers(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.Provider]:
        return self.procurement_repo.list_providers(tenant_id, skip, limit)

    # --- Métodos para SparePart ---

    def create_spare_part(self, spare_part_in: schemas.SparePartCreate, tenant_id: uuid.UUID) -> models.SparePart:
        # Aquí se podría añadir lógica de negocio, como validar que el part_number no exista, etc.
        return self.procurement_repo.create_spare_part(spare_part_in, tenant_id)

    def get_spare_part(self, spare_part_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.SparePart]:
        return self.procurement_repo.get_spare_part(spare_part_id, tenant_id)

    def list_spare_parts(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.SparePart]:
        return self.procurement_repo.list_spare_parts(tenant_id, skip, limit)

    def update_spare_part_stock(self, spare_part_id: uuid.UUID, tenant_id: uuid.UUID, quantity_change: int) -> Optional[models.SparePart]:
        # Lógica de negocio: no permitir stock negativo, etc.
        spare_part = self.procurement_repo.get_spare_part(spare_part_id, tenant_id)
        if not spare_part:
            return None
        
        if spare_part.stock_quantity + quantity_change < 0:
            raise ValueError("Stock cannot be negative.")

        return self.procurement_repo.update_spare_part_stock(spare_part_id, tenant_id, quantity_change)
