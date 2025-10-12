# /app/procurement/service.py
"""
Capa de Servicio para el módulo de Compras (Procurement).

Contiene la lógica de negocio que orquesta las operaciones del repositorio.
"""

from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.procurement import models, schemas
from app.procurement.repository import ProcurementRepository


class ProcurementService:
    """Servicio de negocio para la gestión de compras y proveedores."""

    def __init__(self, db: Session):
        self.db = db
        self.procurement_repo = ProcurementRepository(self.db)

    def create_provider(self, provider_in: schemas.ProviderCreate) -> models.Provider:
        """Crea un nuevo proveedor."""
        return self.procurement_repo.create_provider(provider_in)

    def get_provider(self, provider_id: uuid.UUID) -> Optional[models.Provider]:
        """Obtiene un proveedor por su ID."""
        return self.procurement_repo.get_provider(provider_id)

    def list_providers(self, skip: int = 0, limit: int = 100) -> List[models.Provider]:
        """Lista todos los proveedores activos."""
        return self.procurement_repo.list_providers(skip, limit)

    def update_provider(self, provider_id: uuid.UUID, provider_in: schemas.ProviderUpdate) -> models.Provider:
        """Actualiza un proveedor existente."""
        db_provider = self.get_provider(provider_id)
        if not db_provider:
            raise NotFoundException(f"Proveedor con ID {provider_id} no encontrado.")
        
        return self.procurement_repo.update_provider(db_provider=db_provider, provider_in=provider_in)

    def soft_delete_provider(self, provider_id: uuid.UUID) -> models.Provider:
        """Realiza un borrado lógico (soft delete) de un proveedor."""
        db_provider = self.get_provider(provider_id)
        if not db_provider:
            raise NotFoundException(f"Proveedor con ID {provider_id} no encontrado.")
        
        return self.procurement_repo.soft_delete_provider(db_provider)
