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
from app.core.exceptions import NotFoundException

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

    def get_provider(self, provider_id: uuid.UUID, tenant_id: uuid.UUID) -> models.Provider:
        db_provider = self.procurement_repo.get_provider(provider_id, tenant_id)
        if not db_provider:
            raise NotFoundException("Proveedor no encontrado.")
        return db_provider

    def list_providers(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.Provider]:
        return self.procurement_repo.list_providers(tenant_id, skip, limit)

    def update_provider(self, provider_id: uuid.UUID, provider_in: schemas.ProviderUpdate, tenant_id: uuid.UUID) -> models.Provider:
        db_provider = self.get_provider(provider_id, tenant_id)
        return self.procurement_repo.update_provider(db_provider, provider_in)

    def delete_provider(self, provider_id: uuid.UUID, tenant_id: uuid.UUID) -> models.Provider:
        db_provider = self.get_provider(provider_id, tenant_id)
        return self.procurement_repo.delete_provider(db_provider)

    # --- Métodos para SparePart ---

    def create_spare_part(self, spare_part_in: schemas.SparePartCreate, tenant_id: uuid.UUID) -> models.SparePart:
        return self.procurement_repo.create_spare_part(spare_part_in, tenant_id)

    def get_spare_part(self, spare_part_id: uuid.UUID, tenant_id: uuid.UUID) -> models.SparePart:
        db_spare_part = self.procurement_repo.get_spare_part(spare_part_id, tenant_id)
        if not db_spare_part:
            raise NotFoundException("Repuesto no encontrado.")
        return db_spare_part

    def list_spare_parts(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.SparePart]:
        return self.procurement_repo.list_spare_parts(tenant_id, skip, limit)

    def update_spare_part(self, spare_part_id: uuid.UUID, spare_part_in: schemas.SparePartUpdate, tenant_id: uuid.UUID) -> models.SparePart:
        db_spare_part = self.get_spare_part(spare_part_id, tenant_id)
        return self.procurement_repo.update_spare_part(db_spare_part, spare_part_in)

    def delete_spare_part(self, spare_part_id: uuid.UUID, tenant_id: uuid.UUID) -> models.SparePart:
        db_spare_part = self.get_spare_part(spare_part_id, tenant_id)
        return self.procurement_repo.delete_spare_part(db_spare_part)
