# /app/assets/repository.py
"""
Capa de Repositorio para el módulo de Activos (Assets).

Encapsula toda la lógica de acceso a datos para los modelos Asset, AssetType
y AssetHierarchy.
"""
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from app.assets import models, schemas


class AssetRepository:
    """Realiza operaciones CRUD en la base de datos para el módulo de Activos."""

    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para AssetType ---

    def create_asset_type(self, asset_type_in: schemas.AssetTypeCreate) -> models.AssetType:
        """Crea un nuevo tipo de activo en el catálogo."""
        db_asset_type = models.AssetType(**asset_type_in.model_dump())
        self.db.add(db_asset_type)
        self.db.commit()
        self.db.refresh(db_asset_type)
        return db_asset_type

    def get_asset_type(self, asset_type_id: uuid.UUID) -> Optional[models.AssetType]:
        """Obtiene un tipo de activo por su ID."""
        return self.db.query(models.AssetType).filter(models.AssetType.id == asset_type_id).first()

    def list_asset_types(self, skip: int = 0, limit: int = 100) -> List[models.AssetType]:
        """Lista todos los tipos de activos con paginación."""
        return self.db.query(models.AssetType).offset(skip).limit(limit).all()

    # --- Métodos para Asset (Instancia Física) ---

    def create_asset(self, asset_in: schemas.AssetCreate) -> models.Asset:
        """Registra una nueva instancia física de un activo."""
        db_asset = models.Asset(**asset_in.model_dump())
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def get_asset(self, asset_id: uuid.UUID) -> Optional[models.Asset]:
        """Obtiene una instancia de activo por su ID."""
        return self.db.query(models.Asset).filter(models.Asset.id == asset_id).first()

    # --- Métodos para AssetHierarchy ---

    def add_component_to_hierarchy(
        self, hierarchy_in: schemas.AssetHierarchyCreate
    ) -> models.AssetHierarchy:
        """Añade una relación de componente a la jerarquía (BOM)."""
        db_hierarchy = models.AssetHierarchy(**hierarchy_in.model_dump())
        self.db.add(db_hierarchy)
        self.db.commit()
        self.db.refresh(db_hierarchy)
        return db_hierarchy
