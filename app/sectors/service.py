# /app/sectors/service.py
"""
Capa de Servicio para el módulo de Sectores.
"""
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.sectors import models, schemas
from app.sectors.repository import SectorRepository
from app.core.exceptions import NotFoundException, ConflictException
from app.auditing.service import AuditService
from app.identity.models import User

class SectorService:
    """Servicio de negocio para la gestión de sectores."""

    def __init__(self, db: Session, audit_service: AuditService):
        self.db = db
        self.audit_service = audit_service
        self.sector_repo = SectorRepository(self.db)

    def create_sector(self, sector_in: schemas.SectorCreate, tenant_id: uuid.UUID, user: User) -> models.Sector:
        if sector_in.parent_id:
            parent = self.sector_repo.get_sector(sector_in.parent_id, tenant_id)
            if not parent:
                raise NotFoundException(f"El sector padre con ID {sector_in.parent_id} no existe.")
        
        sector = self.sector_repo.create_sector(sector_in, tenant_id)
        self.audit_service.log_operation(user, "CREATE_SECTOR", sector)
        return sector

    def get_sector(self, sector_id: uuid.UUID, tenant_id: uuid.UUID) -> models.Sector:
        sector = self.sector_repo.get_sector(sector_id, tenant_id)
        if not sector:
            raise NotFoundException("Sector no encontrado.")
        return sector

    def list_sectors(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100, parent_id: Optional[uuid.UUID] = None) -> List[models.Sector]:
        return self.sector_repo.list_sectors(tenant_id, skip, limit, parent_id)

    def update_sector(self, sector_id: uuid.UUID, sector_in: schemas.SectorUpdate, tenant_id: uuid.UUID, user: User) -> models.Sector:
        db_sector = self.get_sector(sector_id, tenant_id)
        
        if sector_in.parent_id:
            if sector_in.parent_id == sector_id:
                raise ConflictException("Un sector no puede ser su propio padre.")
            parent = self.sector_repo.get_sector(sector_in.parent_id, tenant_id)
            if not parent:
                raise NotFoundException(f"El sector padre con ID {sector_in.parent_id} no existe.")

        updated_sector = self.sector_repo.update_sector(db_sector, sector_in)
        self.audit_service.log_operation(user, "UPDATE_SECTOR", updated_sector, details=sector_in.model_dump(exclude_unset=True))
        return updated_sector

    def delete_sector(self, sector_id: uuid.UUID, tenant_id: uuid.UUID, user: User) -> models.Sector:
        db_sector = self.get_sector(sector_id, tenant_id)
        
        if self.sector_repo.has_active_children(sector_id):
            raise ConflictException("No se puede eliminar un sector que tiene sub-sectores activos. Reasigne o elimine los sub-sectores primero.")
            
        # TODO: Validar también si tiene activos asignados (requeriría inyectar AssetRepository)

        deleted_sector = self.sector_repo.delete_sector(db_sector)
        self.audit_service.log_operation(user, "DELETE_SECTOR", deleted_sector)
        return deleted_sector
