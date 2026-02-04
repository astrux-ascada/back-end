# /app/sectors/repository.py
"""
Capa de Repositorio para el módulo de Sectores.
"""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.sectors import models, schemas

class SectorRepository:
    """Realiza operaciones CRUD para los sectores."""

    def __init__(self, db: Session):
        self.db = db

    def create_sector(self, sector_in: schemas.SectorCreate, tenant_id: uuid.UUID) -> models.Sector:
        db_sector = models.Sector(**sector_in.model_dump(), tenant_id=tenant_id)
        self.db.add(db_sector)
        self.db.commit()
        self.db.refresh(db_sector)
        return db_sector

    def get_sector(self, sector_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.Sector]:
        return self.db.query(models.Sector).filter(
            models.Sector.id == sector_id,
            models.Sector.tenant_id == tenant_id
        ).first()

    def list_sectors(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100, parent_id: Optional[uuid.UUID] = None) -> List[models.Sector]:
        query = self.db.query(models.Sector).filter(
            models.Sector.tenant_id == tenant_id,
            models.Sector.is_active == True
        )
        if parent_id:
            query = query.filter(models.Sector.parent_id == parent_id)
            
        return query.offset(skip).limit(limit).all()

    def update_sector(self, db_sector: models.Sector, sector_in: schemas.SectorUpdate) -> models.Sector:
        update_data = sector_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sector, field, value)
        self.db.add(db_sector)
        self.db.commit()
        self.db.refresh(db_sector)
        return db_sector

    def delete_sector(self, db_sector: models.Sector) -> models.Sector:
        db_sector.is_active = False
        self.db.add(db_sector)
        self.db.commit()
        self.db.refresh(db_sector)
        return db_sector
    
    def has_active_children(self, sector_id: uuid.UUID) -> bool:
        """Verifica si un sector tiene sub-sectores activos."""
        count = self.db.query(models.Sector).filter(
            models.Sector.parent_id == sector_id,
            models.Sector.is_active == True
        ).count()
        return count > 0
