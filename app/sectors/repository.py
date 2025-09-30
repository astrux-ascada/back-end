# /app/sectors/repository.py
"""
Capa de Repositorio para el módulo de Sectores.
"""

from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from app.sectors import models, schemas


class SectorRepository:
    """Realiza operaciones CRUD en la base de datos para el módulo de Sectores."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, sector_id: uuid.UUID) -> Optional[models.Sector]:
        """Obtiene un sector por su ID."""
        return self.db.query(models.Sector).filter(models.Sector.id == sector_id).first()

    def get_by_ids(self, sector_ids: List[uuid.UUID]) -> List[models.Sector]:
        """Busca una lista de sectores por sus IDs."""
        return self.db.query(models.Sector).filter(models.Sector.id.in_(sector_ids)).all()

    def create(self, sector_in: schemas.SectorCreate) -> models.Sector:
        """Crea un nuevo sector."""
        db_sector = models.Sector(**sector_in.model_dump())
        self.db.add(db_sector)
        self.db.commit()
        self.db.refresh(db_sector)
        return db_sector

    def list(self, skip: int = 0, limit: int = 100) -> List[models.Sector]:
        """Lista todos los sectores."""
        return self.db.query(models.Sector).offset(skip).limit(limit).all()
