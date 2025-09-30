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
# --- MEJORA: Importar el mapper centralizado ---
from app.assets.mappers import map_asset_to_dto


class AssetService:
    """Servicio de negocio para la gestión de activos."""

    def __init__(self, db: Session):
        self.db = db
        self.asset_repo = AssetRepository(self.db)

    # El método _map_asset_to_dto ha sido movido a mappers.py

    def create_asset(self, asset_in: schemas.AssetCreate) -> schemas.AssetReadDTO:
        db_asset = self.asset_repo.create_asset(asset_in)
        full_asset = self.asset_repo.get_asset(db_asset.id)
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

    def update_asset_status(self, asset_id: uuid.UUID, status_update: schemas.AssetStatusUpdate) -> Optional[schemas.AssetReadDTO]:
        updated_asset = self.asset_repo.update_asset_status(asset_id, status_update.status)
        if updated_asset:
            return map_asset_to_dto(updated_asset, self.asset_repo)
        return None

    # --- Métodos para AssetType y Hierarchy ---

    def create_asset_type(self, asset_type_in: schemas.AssetTypeCreate) -> models.AssetType:
        return self.asset_repo.create_asset_type(asset_type_in)

    def add_component_to_hierarchy(self, hierarchy_in: schemas.AssetHierarchyCreate) -> models.AssetHierarchy:
        return self.asset_repo.add_component_to_hierarchy(hierarchy_in)
