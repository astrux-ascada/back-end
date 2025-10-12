# /app/procurement/repository.py
"""
Capa de Repositorio para el módulo de Compras (Procurement).

Encapsula la lógica de acceso a datos para las entidades del módulo,
comenzando por Provider.
"""

from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from app.procurement import models, schemas


class ProcurementRepository:
    """Realiza operaciones CRUD en la base de datos para el módulo de Compras."""

    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para Provider ---

    def create_provider(self, provider_in: schemas.ProviderCreate) -> models.Provider:
        """Crea un nuevo proveedor en la base de datos."""
        db_provider = models.Provider(**provider_in.model_dump())
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def get_provider(self, provider_id: uuid.UUID) -> Optional[models.Provider]:
        """Obtiene un proveedor por su ID, sin importar si está activo o no."""
        return self.db.query(models.Provider).filter(models.Provider.id == provider_id).first()

    def list_providers(self, skip: int = 0, limit: int = 100) -> List[models.Provider]:
        """Lista todos los proveedores activos con paginación."""
        return self.db.query(models.Provider).filter(models.Provider.is_active == True).offset(skip).limit(limit).all()

    def update_provider(self, db_provider: models.Provider, provider_in: schemas.ProviderUpdate) -> models.Provider:
        """Actualiza un proveedor existente en la base de datos."""
        update_data = provider_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_provider, field, value)
        
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def soft_delete_provider(self, db_provider: models.Provider) -> models.Provider:
        """Realiza un borrado lógico (soft delete) de un proveedor."""
        db_provider.is_active = False
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider
