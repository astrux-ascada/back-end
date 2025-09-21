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
        """Obtiene un proveedor por su ID."""
        return self.db.query(models.Provider).filter(models.Provider.id == provider_id).first()

    def list_providers(self, skip: int = 0, limit: int = 100) -> List[models.Provider]:
        """Lista todos los proveedores con paginación."""
        return self.db.query(models.Provider).offset(skip).limit(limit).all()
