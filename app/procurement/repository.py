# /app/procurement/repository.py
"""
Capa de Repositorio para el módulo de Compras (Procurement).
"""

from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from app.procurement import models, schemas


class ProcurementRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para Provider ---

    def create_provider(self, provider_in: schemas.ProviderCreate) -> models.Provider:
        db_provider = models.Provider(**provider_in.model_dump())
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def get_provider(self, provider_id: uuid.UUID) -> Optional[models.Provider]:
        return self.db.query(models.Provider).filter(models.Provider.id == provider_id).first()

    def list_providers(self, skip: int = 0, limit: int = 100) -> List[models.Provider]:
        return self.db.query(models.Provider).filter(models.Provider.is_active == True).offset(skip).limit(limit).all()

    def update_provider(self, db_provider: models.Provider, provider_in: schemas.ProviderUpdate) -> models.Provider:
        update_data = provider_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_provider, field, value)
        
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def soft_delete_provider(self, db_provider: models.Provider) -> models.Provider:
        db_provider.is_active = False
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    # --- Métodos para SparePart ---

    def create_spare_part(self, part_in: schemas.SparePartCreate) -> models.SparePart:
        db_part = models.SparePart(**part_in.model_dump())
        self.db.add(db_part)
        self.db.commit()
        self.db.refresh(db_part)
        return db_part

    def get_spare_part(self, part_id: uuid.UUID) -> Optional[models.SparePart]:
        return self.db.query(models.SparePart).filter(models.SparePart.id == part_id).first()

    def list_spare_parts(self, skip: int = 0, limit: int = 100) -> List[models.SparePart]:
        return self.db.query(models.SparePart).filter(models.SparePart.is_active == True).offset(skip).limit(limit).all()

    def update_spare_part(self, db_part: models.SparePart, part_in: schemas.SparePartUpdate) -> models.SparePart:
        update_data = part_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_part, field, value)

        self.db.add(db_part)
        self.db.commit()
        self.db.refresh(db_part)
        return db_part
