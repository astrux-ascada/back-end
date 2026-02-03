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
    def create_asset_type(self, asset_type_in: schemas.AssetTypeCreate, tenant_id: uuid.UUID) -> models.AssetType:
        db_asset_type = models.AssetType(**asset_type_in.model_dump(), tenant_id=tenant_id)
        self.db.add(db_asset_type)
        self.db.commit()
        self.db.refresh(db_asset_type)
        return db_asset_type

    # --- Métodos para Asset (Instancia Física) ---

    def create_asset(self, asset_in: schemas.AssetCreate, tenant_id: uuid.UUID) -> models.Asset:
        db_asset = models.Asset(**asset_in.model_dump(), tenant_id=tenant_id)
        self.db.add(db_asset)
        self.db.commit()
        # No hacemos refresh simple porque necesitamos las relaciones.
        # Hacemos una query completa para devolver el objeto listo para el DTO.
        return self.get_asset(db_asset.id, tenant_id)

    def get_asset(self, asset_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.Asset]:
        return (
            self.db.query(models.Asset)
            .options(joinedload(models.Asset.asset_type), joinedload(models.Asset.sector))
            .filter(models.Asset.id == asset_id, models.Asset.tenant_id == tenant_id) # Filtro por tenant
            .first()
        )

    def list_assets(
        self,
        tenant_id: uuid.UUID,
        skip: int = 0, 
        limit: int = 100, 
        category: Optional[str] = None, 
        sector_id: Optional[uuid.UUID] = None
    ) -> List[models.Asset]:
        query = self.db.query(models.Asset).options(joinedload(models.Asset.asset_type), joinedload(models.Asset.sector))
        
        # Filtro principal por tenant
        query = query.filter(models.Asset.tenant_id == tenant_id)

        if category:
            query = query.join(models.AssetType).filter(models.AssetType.category == category)
        if sector_id:
            query = query.filter(models.Asset.sector_id == sector_id)
            
        return query.offset(skip).limit(limit).all()

    def update_asset(self, db_asset: models.Asset, asset_in: schemas.AssetUpdate) -> models.Asset:
        """Actualiza una instancia de activo con los datos proporcionados."""
        update_data = asset_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_asset, field, value)
        
        self.db.add(db_asset)
        self.db.commit()
        # Devolvemos el objeto recargado con relaciones
        return self.get_asset(db_asset.id, db_asset.tenant_id)

    def update_asset_status(self, asset_id: uuid.UUID, tenant_id: uuid.UUID, new_status: str) -> Optional[models.Asset]:
        """Actualiza el campo de estado de un activo específico."""
        db_asset = self.db.query(models.Asset).filter(models.Asset.id == asset_id, models.Asset.tenant_id == tenant_id).first()
        if db_asset:
            db_asset.status = new_status
            self.db.commit()
            return self.get_asset(asset_id, tenant_id) # Devolver con relaciones
        return None

    # --- Métodos para AssetHierarchy ---
    def add_component_to_hierarchy(self, hierarchy_in: schemas.AssetHierarchyCreate, tenant_id: uuid.UUID) -> models.AssetHierarchy:
        db_hierarchy = models.AssetHierarchy(**hierarchy_in.model_dump())
        self.db.add(db_hierarchy)
        self.db.commit()
        self.db.refresh(db_hierarchy)
        return db_hierarchy

    def get_parent_asset_type(self, child_asset_type_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.AssetType]:
        child_type = self.db.query(models.AssetType).filter(models.AssetType.id == child_asset_type_id, models.AssetType.tenant_id == tenant_id).first()
        if not child_type:
            return None

        parent_assoc = self.db.query(models.AssetHierarchy).filter(models.AssetHierarchy.child_asset_type_id == child_asset_type_id).first()
        if parent_assoc:
            return self.db.query(models.AssetType).filter(models.AssetType.id == parent_assoc.parent_asset_type_id, models.AssetType.tenant_id == tenant_id).first()
        return None
