# /app/procurement/repository.py
"""
Capa de Repositorio para el módulo de Compras (Procurement).
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

    def create_provider(self, provider_in: schemas.ProviderCreate, tenant_id: uuid.UUID) -> models.Provider:
        db_provider = models.Provider(**provider_in.model_dump(), tenant_id=tenant_id)
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def get_provider(self, provider_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.Provider]:
        return self.db.query(models.Provider).filter(
            models.Provider.id == provider_id, 
            models.Provider.tenant_id == tenant_id
        ).first()

    def list_providers(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100, include_inactive: bool = False) -> List[models.Provider]:
        query = self.db.query(models.Provider).filter(models.Provider.tenant_id == tenant_id)
        if not include_inactive:
            query = query.filter(models.Provider.is_active == True)
        return query.offset(skip).limit(limit).all()

    def update_provider(self, db_provider: models.Provider, provider_in: schemas.ProviderUpdate) -> models.Provider:
        update_data = provider_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_provider, field, value)
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def delete_provider(self, db_provider: models.Provider) -> models.Provider:
        db_provider.is_active = False
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    # --- Métodos para SparePart ---

    def create_spare_part(self, spare_part_in: schemas.SparePartCreate, tenant_id: uuid.UUID) -> models.SparePart:
        db_spare_part = models.SparePart(**spare_part_in.model_dump(), tenant_id=tenant_id)
        self.db.add(db_spare_part)
        self.db.commit()
        self.db.refresh(db_spare_part)
        return db_spare_part

    def get_spare_part(self, spare_part_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.SparePart]:
        return self.db.query(models.SparePart).filter(
            models.SparePart.id == spare_part_id, 
            models.SparePart.tenant_id == tenant_id
        ).first()

    def list_spare_parts(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100, include_inactive: bool = False) -> List[models.SparePart]:
        query = self.db.query(models.SparePart).filter(models.SparePart.tenant_id == tenant_id)
        if not include_inactive:
            query = query.filter(models.SparePart.is_active == True)
        return query.offset(skip).limit(limit).all()

    def update_spare_part(self, db_spare_part: models.SparePart, spare_part_in: schemas.SparePartUpdate) -> models.SparePart:
        update_data = spare_part_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_spare_part, field, value)
        self.db.add(db_spare_part)
        self.db.commit()
        self.db.refresh(db_spare_part)
        return db_spare_part

    def delete_spare_part(self, db_spare_part: models.SparePart) -> models.SparePart:
        db_spare_part.is_active = False
        self.db.add(db_spare_part)
        self.db.commit()
        self.db.refresh(db_spare_part)
        return db_spare_part
