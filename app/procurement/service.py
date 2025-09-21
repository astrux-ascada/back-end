# /app/procurement/service.py
"""
Capa de Servicio para el módulo de Compras (Procurement).

Contiene la lógica de negocio que orquesta las operaciones del repositorio.
"""

from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.procurement import models, schemas
from app.procurement.repository import ProcurementRepository


class ProcurementService:
    """Servicio de negocio para la gestión de compras y proveedores."""

    def __init__(self, db: Session):
        self.db = db
        self.procurement_repo = ProcurementRepository(self.db)

    def create_provider(self, provider_in: schemas.ProviderCreate) -> models.Provider:
        """Crea un nuevo proveedor.

        En el futuro, podría incluir lógica para validar datos del proveedor
        contra sistemas externos o para notificar al equipo de compras.
        """
        return self.procurement_repo.create_provider(provider_in)

    def get_provider(self, provider_id: uuid.UUID) -> Optional[models.Provider]:
        """Obtiene un proveedor por su ID."""
        return self.procurement_repo.get_provider(provider_id)

    def list_providers(self, skip: int = 0, limit: int = 100) -> List[models.Provider]:
        """Lista todos los proveedores."""
        return self.procurement_repo.list_providers(skip, limit)
