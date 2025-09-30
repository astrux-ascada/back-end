# /app/sectors/service.py
"""
Capa de Servicio para el módulo de Sectores.
"""

from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.sectors import models, schemas
from app.sectors.repository import SectorRepository


class SectorService:
    """Servicio de negocio para la gestión de sectores."""

    def __init__(self, db: Session):
        self.db = db
        self.sector_repo = SectorRepository(self.db)

    def create_sector(self, sector_in: schemas.SectorCreate) -> models.Sector:
        """Crea un nuevo sector."""
        return self.sector_repo.create(sector_in)

    def list_sectors(self, skip: int = 0, limit: int = 100) -> List[models.Sector]:
        """Lista todos los sectores."""
        return self.sector_repo.list(skip, limit)
