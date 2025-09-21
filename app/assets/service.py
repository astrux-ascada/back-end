# /app/assets/service.py
"""
Capa de Servicio para el módulo de Activos (Assets).

Contiene la lógica de negocio que orquesta las operaciones del repositorio
para realizar tareas complejas relacionadas con los activos.
"""

from sqlalchemy.orm import Session
import uuid

from app.assets import models, schemas
from app.assets.repository import AssetRepository
# from app.core.exceptions import NotFoundException  # Lo usaremos en el futuro


class AssetService:
    """Servicio de negocio para la gestión de activos."""

    def __init__(self, db: Session):
        self.db = db
        self.asset_repo = AssetRepository(self.db)

    def create_asset_type(self, asset_type_in: schemas.AssetTypeCreate) -> models.AssetType:
        """Crea un nuevo tipo de activo.

        Por ahora, delega directamente en el repositorio. En el futuro, podría
        añadir lógica como la validación de categorías contra una lista permitida.
        """
        return self.asset_repo.create_asset_type(asset_type_in)

    def create_asset(self, asset_in: schemas.AssetCreate) -> models.Asset:
        """Crea una nueva instancia de activo.

        Aquí se podría añadir lógica para verificar que el asset_type_id existe
        antes de intentar crear el activo.
        """
        # Lógica de negocio futura: verificar si self.asset_repo.get_asset_type(asset_in.asset_type_id) existe.
        return self.asset_repo.create_asset(asset_in)

    def add_component(self, hierarchy_in: schemas.AssetHierarchyCreate) -> models.AssetHierarchy:
        """Añade un componente a la jerarquía de un tipo de activo.

        Lógica de negocio futura: verificar que tanto el padre como el hijo existen.
        """
        return self.asset_repo.add_component_to_hierarchy(hierarchy_in)

    def get_asset_type_with_hierarchy(self, asset_type_id: uuid.UUID) -> models.AssetType | None:
        """Obtiene un tipo de activo y enriquece el objeto con su jerarquía."""
        # Esta es lógica de negocio: combina múltiples llamadas al repositorio.
        asset_type = self.asset_repo.get_asset_type(asset_type_id)
        # En el futuro, aquí poblaríamos los campos .children y .parents
        # haciendo más llamadas al repositorio para obtener los datos de la jerarquía.
        return asset_type
