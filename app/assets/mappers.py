# /app/assets/mappers.py
"""
Funciones de mapeo para el módulo de Activos.

Contiene la lógica para transformar los modelos de la base de datos (SQLAlchemy)
en los DTOs (Data Transfer Objects) que se usan en la API (Pydantic).
"""

from app.assets import models, schemas
from app.assets.repository import AssetRepository


def map_asset_to_dto(asset: models.Asset, asset_repo: AssetRepository) -> schemas.AssetReadDTO:
    """Mapea un objeto Asset de SQLAlchemy al DTO plano de la API."""
    # Obtener el ID del padre usando el repositorio
    parent_type = asset_repo.get_parent_asset_type(asset.asset_type.id)
    parent_id = parent_type.id if parent_type else None

    # Construir el DTO
    return schemas.AssetReadDTO(
        id=asset.id,
        # --- CORREGIDO: El estado de actividad depende del status del activo, no de su tipo.
        is_active=(asset.status.lower() == 'operational'),
        created_at=asset.created_at,
        updated_at=asset.updated_at,
        status=asset.status,
        properties=asset.properties,
        name=asset.asset_type.name,
        description=asset.asset_type.description,
        type=asset.asset_type.category,
        sector=asset.sector,
        parent_id=parent_id
    )
