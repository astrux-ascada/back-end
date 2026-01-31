# /app/procurement/service.py
"""
Capa de Servicio para el módulo de Compras (Procurement).

Gestiona la lógica de negocio para Proveedores y Repuestos.
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

    # --- Provider Services ---

    def create_provider(self, provider_in: schemas.ProviderCreate) -> models.Provider:
        """Crea un nuevo proveedor."""
        logger.info(f"Creando nuevo proveedor: {provider_in.name}")
        provider = self.repo.create_provider(provider_in)
        logger.info(f"Proveedor '{provider.name}' creado con ID: {provider.id}")
        return provider

    def get_provider(self, provider_id: uuid.UUID) -> Optional[models.Provider]:
        """Obtiene un proveedor por su ID."""
        return self.repo.get_provider(provider_id)

    def list_providers(self, skip: int = 0, limit: int = 100) -> List[models.Provider]:
        """Lista todos los proveedores activos."""
        return self.repo.list_providers(skip, limit)

    def update_provider(self, provider_id: uuid.UUID, provider_in: schemas.ProviderUpdate) -> models.Provider:
        """Actualiza un proveedor existente."""
        logger.info(f"Actualizando proveedor {provider_id} con datos: {provider_in.model_dump(exclude_unset=True)}")
        db_provider = self.get_provider(provider_id)
        if not db_provider:
            logger.warning(f"Intento de actualizar proveedor inexistente: {provider_id}")
            raise NotFoundException(f"Proveedor con ID {provider_id} no encontrado.")
        return self.repo.update_provider(db_provider=db_provider, provider_in=provider_in)

    def soft_delete_provider(self, provider_id: uuid.UUID) -> models.Provider:
        """Realiza un borrado lógico (soft delete) de un proveedor."""
        logger.info(f"Desactivando proveedor {provider_id}")
        db_provider = self.get_provider(provider_id)
        if not db_provider:
            logger.warning(f"Intento de desactivar proveedor inexistente: {provider_id}")
            raise NotFoundException(f"Proveedor con ID {provider_id} no encontrado.")
        return self.repo.soft_delete_provider(db_provider)

    # --- Spare Part Services ---

    def create_spare_part(self, part_in: schemas.SparePartCreate) -> models.SparePart:
        """Crea un nuevo repuesto en el catálogo."""
        logger.info(f"Creando nuevo repuesto: {part_in.name}")
        part = self.repo.create_spare_part(part_in)
        logger.info(f"Repuesto '{part.name}' creado con ID: {part.id}")
        return part

    def get_spare_part(self, part_id: uuid.UUID) -> Optional[models.SparePart]:
        """Obtiene un repuesto por su ID."""
        return self.repo.get_spare_part(part_id)

    def list_spare_parts(self, skip: int = 0, limit: int = 100) -> List[models.SparePart]:
        """Lista todos los repuestos activos."""
        return self.repo.list_spare_parts(skip, limit)

    def update_spare_part(self, part_id: uuid.UUID, part_in: schemas.SparePartUpdate) -> models.SparePart:
        """Actualiza un repuesto existente."""
        logger.info(f"Actualizando repuesto {part_id} con datos: {part_in.model_dump(exclude_unset=True)}")
        db_part = self.get_spare_part(part_id)
        if not db_part:
            logger.warning(f"Intento de actualizar repuesto inexistente: {part_id}")
            raise NotFoundException(f"Repuesto con ID {part_id} no encontrado.")
        return self.repo.update_spare_part(db_part=db_part, part_in=part_in)
