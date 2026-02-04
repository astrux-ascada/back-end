# /app/core_engine/repository.py
"""
Capa de Repositorio para el Core Engine.
"""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.core_engine import models, schemas

class CoreEngineRepository:
    """Realiza operaciones CRUD para las entidades del Core Engine."""

    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para DataSource ---

    def create_data_source(self, data_source_in: schemas.DataSourceCreate, tenant_id: uuid.UUID) -> models.DataSource:
        db_obj = models.DataSource(**data_source_in.model_dump(), tenant_id=tenant_id)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_data_source(self, data_source_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.DataSource]:
        return self.db.query(models.DataSource).filter(
            models.DataSource.id == data_source_id,
            models.DataSource.tenant_id == tenant_id
        ).first()

    def list_data_sources(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.DataSource]:
        return self.db.query(models.DataSource).filter(
            models.DataSource.tenant_id == tenant_id,
            models.DataSource.is_active == True
        ).offset(skip).limit(limit).all()

    def update_data_source(self, db_obj: models.DataSource, obj_in: schemas.DataSourceUpdate) -> models.DataSource:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete_data_source(self, db_obj: models.DataSource) -> models.DataSource:
        db_obj.is_active = False
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
