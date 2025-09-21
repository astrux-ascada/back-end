# /app/core_engine/repository.py
"""
Capa de Repositorio para el módulo Core Engine.

Encapsula la lógica de acceso a datos para las entidades del módulo,
comenzando por DataSource.
"""

from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from app.core_engine import models, schemas


class CoreEngineRepository:
    """Realiza operaciones CRUD en la base de datos para el módulo Core Engine."""

    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para DataSource ---

    def create_data_source(self, data_source_in: schemas.DataSourceCreate) -> models.DataSource:
        """Crea una nueva fuente de datos en la base de datos."""
        db_data_source = models.DataSource(**data_source_in.model_dump())
        self.db.add(db_data_source)
        self.db.commit()
        self.db.refresh(db_data_source)
        return db_data_source

    def get_data_source(self, data_source_id: uuid.UUID) -> Optional[models.DataSource]:
        """Obtiene una fuente de datos por su ID."""
        return self.db.query(models.DataSource).filter(models.DataSource.id == data_source_id).first()

    def list_data_sources(self, skip: int = 0, limit: int = 100) -> List[models.DataSource]:
        """Lista todas las fuentes de datos con paginación."""
        return self.db.query(models.DataSource).offset(skip).limit(limit).all()

    def list_active_data_sources(self) -> List[models.DataSource]:
        """Obtiene una lista de todas las fuentes de datos marcadas como activas."""
        return self.db.query(models.DataSource).filter(models.DataSource.is_active == True).all()
