# /app/assets/service.py
"""
Capa de Servicio para el módulo de Activos (Assets).

Contiene la lógica de negocio que orquesta las operaciones del repositorio
y transforma los modelos de la base de datos en los DTOs para la API.
"""

from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.assets import models, schemas
from app.assets.repository import AssetRepository
from app.assets.mappers import map_asset_to_dto
from app.auditing.service import AuditService
from app.identity.models import User


class AssetService:
    """Servicio de negocio para la gestión de activos."""

    def __init__(self, db: Session, audit_service: AuditService):
        self.db = db
        self.audit_service = audit_service
        self.asset_repo = AssetRepository(self.db)

    def create_asset(self, asset_in: schemas.AssetCreate, current_user: User) -> schemas.AssetReadDTO:
        db_asset = self.asset_repo.create_asset(asset_in)
        full_asset = self.asset_repo.get_asset(db_asset.id)
        
        self.audit_service.log_operation(
            user=current_user,
            action="CREATE_ASSET",
            entity=full_asset
        )
        return map_asset_to_dto(full_asset, self.asset_repo)

    def get_asset(self, asset_id: uuid.UUID) -> Optional[schemas.AssetReadDTO]:
        asset = self.asset_repo.get_asset(asset_id)
        if asset:
            return map_asset_to_dto(asset, self.asset_repo)
        return None

    def list_assets(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        category: Optional[str] = None, 
        sector_id: Optional[uuid.UUID] = None
    ) -> List[schemas.AssetReadDTO]:
        assets = self.asset_repo.list_assets(skip, limit, category, sector_id)
        return [map_asset_to_dto(asset, self.asset_repo) for asset in assets]

    def update_asset(
        self, 
        asset_id: uuid.UUID, 
        asset_in: schemas.AssetUpdate, 
        current_user: User
    ) -> Optional[schemas.AssetReadDTO]:
        """Actualiza un activo existente y registra la operación en la auditoría."""
        db_asset = self.asset_repo.get_asset(asset_id)
        if not db_asset:
            return None

        updated_asset = self.asset_repo.update_asset(db_asset=db_asset, asset_in=asset_in)

        self.audit_service.log_operation(
            user=current_user,
            action="UPDATE_ASSET",
            entity=updated_asset,
            details=asset_in.model_dump(exclude_unset=True)
        )
        
        full_updated_asset = self.asset_repo.get_asset(updated_asset.id)
        return map_asset_to_dto(full_updated_asset, self.asset_repo)

    def update_asset_status(
        self, 
        asset_id: uuid.UUID, 
        status_update: schemas.AssetStatusUpdate, 
        current_user: User
    ) -> Optional[schemas.AssetReadDTO]:
        """Actualiza el estado de un activo y registra la operación en la auditoría."""
        asset_before_update = self.asset_repo.get_asset(asset_id)
        if not asset_before_update:
            return None
        
        old_status = asset_before_update.status
        new_status = status_update.status

        updated_asset = self.asset_repo.update_asset_status(asset_id, new_status)
        
        if updated_asset:
            self.audit_service.log_operation(
                user=current_user,
                action="UPDATE_STATUS",
                entity=updated_asset,
                details={"from": old_status, "to": new_status}
            )
            return map_asset_to_dto(updated_asset, self.asset_repo)
        return None

    # --- Métodos para AssetType y Hierarchy ---

    def create_asset_type(self, asset_type_in: schemas.AssetTypeCreate) -> models.AssetType:
        return self.asset_repo.create_asset_type(asset_type_in)

    def add_component_to_hierarchy(self, hierarchy_in: schemas.AssetHierarchyCreate) -> models.AssetHierarchy:
        return self.asset_repo.add_component_to_hierarchy(hierarchy_in)
