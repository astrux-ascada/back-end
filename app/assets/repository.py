# /app/assets/repository.py
"""
Capa de Repositorio para el módulo de Activos (Assets).

Encapsula toda la lógica de acceso a datos para los modelos Asset, AssetType
y AssetHierarchy, con capacidades de filtrado y carga eficiente.
"""
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session, joinedload

from app.assets import models, schemas


class AssetRepository:
    """Realiza operaciones CRUD en la base de datos para el módulo de Activos."""

    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para AssetType ---

    def create_asset_type(self, asset_type_in: schemas.AssetTypeCreate) -> models.AssetType:
        db_asset_type = models.AssetType(**asset_type_in.model_dump())
        self.db.add(db_asset_type)
        self.db.commit()
        self.db.refresh(db_asset_type)
        return db_asset_type

    # --- Métodos para Asset (Instancia Física) ---

    def create_asset(self, asset_in: schemas.AssetCreate) -> models.Asset:
        db_asset = models.Asset(**asset_in.model_dump())
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def get_asset(self, asset_id: uuid.UUID) -> Optional[models.Asset]:
        return (
            self.db.query(models.Asset)
            .options(joinedload(models.Asset.asset_type), joinedload(models.Asset.sector))
            .filter(models.Asset.id == asset_id)
            .first()
        )

    def list_assets(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        category: Optional[str] = None, 
        sector_id: Optional[uuid.UUID] = None
    ) -> List[models.Asset]:
        query = self.db.query(models.Asset).options(joinedload(models.Asset.asset_type), joinedload(models.Asset.sector))
        if category:
            query = query.join(models.AssetType).filter(models.AssetType.category == category)
        if sector_id:
            query = query.filter(models.Asset.sector_id == sector_id)
        return query.offset(skip).limit(limit).all()

    def update_asset_status(self, asset_id: uuid.UUID, new_status: str) -> Optional[models.Asset]:
        """Actualiza el campo de estado de un activo específico."""
        db_asset = self.get_asset(asset_id) # Reutilizamos get_asset para obtener el objeto
        if db_asset:
            db_asset.status = new_status
            self.db.commit()
            self.db.refresh(db_asset)
        return db_asset

    # --- Métodos para AssetHierarchy ---

    def add_component_to_hierarchy(self, hierarchy_in: schemas.AssetHierarchyCreate) -> models.AssetHierarchy:
        db_hierarchy = models.AssetHierarchy(**hierarchy_in.model_dump())
        self.db.add(db_hierarchy)
        self.db.commit()
        self.db.refresh(db_hierarchy)
        return db_hierarchy

    def get_parent_asset_type(self, child_asset_type_id: uuid.UUID) -> Optional[models.AssetType]:
        parent_assoc = self.db.query(models.AssetHierarchy).filter(models.AssetHierarchy.child_asset_type_id == child_asset_type_id).first()
        if parent_assoc:
            return self.db.query(models.AssetType).filter(models.AssetType.id == parent_assoc.parent_asset_type_id).first()
        return None
