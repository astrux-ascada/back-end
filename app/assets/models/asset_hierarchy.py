# /app/assets/models/asset_hierarchy.py
"""
Modelo de la base de datos para la entidad AssetHierarchy.

Define la estructura jerárquica (Bill of Materials) entre los Tipos de Activos.
"""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class AssetHierarchy(Base):
    """Modelo SQLAlchemy para la Jerarquía de Activos (BOM)."""
    __tablename__ = "asset_hierarchy"

    # --- Claves Foráneas Compuestas como Clave Primaria ---
    # Un tipo de activo padre solo puede tener una entrada para un tipo de activo hijo.
    parent_asset_type_id = Column(UUID(as_uuid=True), ForeignKey("asset_types.id"), primary_key=True)
    child_asset_type_id = Column(UUID(as_uuid=True), ForeignKey("asset_types.id"), primary_key=True)

    # --- Cantidad ---
    # Cuántos componentes hijos se necesitan para el padre.
    quantity = Column(Integer, nullable=False, default=1)
