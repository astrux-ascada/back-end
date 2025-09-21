# /app/assets/schemas.py
"""
Esquemas Pydantic para el módulo de Activos (Assets).

Define los contratos de datos para la API, cubriendo AssetType, Asset y AssetHierarchy.
"""
import uuid
from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# --- Esquemas para AssetType (El Catálogo) ---

class AssetTypeBase(BaseModel):
    name: str = Field(..., example="Servo Motor X5")
    description: Optional[str] = Field(None, example="Motor de alta precisión para brazos robóticos.")
    manufacturer: Optional[str] = Field(None, example="Astruxa Dynamics")
    model_number: Optional[str] = Field(None, example="ASX-MTR-X5")
    category: Optional[str] = Field(None, example="Motor", index=True)

class AssetTypeCreate(AssetTypeBase):
    pass

class AssetTypeRead(AssetTypeBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


# --- Esquemas para Asset (La Instancia Física) ---

class AssetBase(BaseModel):
    asset_type_id: uuid.UUID = Field(..., description="ID del tipo de activo del catálogo.")
    serial_number: Optional[str] = Field(None, example="SN-A5B2-C3D4-E5F6")
    location: Optional[str] = Field(None, example="Línea 3, Estación 2, Brazo Izquierdo")
    status: str = Field("operational", example="operational")
    installed_at: Optional[date] = None
    last_maintenance_at: Optional[date] = None
    warranty_expires_at: Optional[date] = None

class AssetCreate(AssetBase):
    pass

class AssetRead(AssetBase):
    id: uuid.UUID
    created_at: datetime
    asset_type: AssetTypeRead  # Anida la información del tipo de activo

    class Config:
        from_attributes = True


# --- Esquemas para AssetHierarchy (La Jerarquía) ---

class AssetHierarchyBase(BaseModel):
    parent_asset_type_id: uuid.UUID
    child_asset_type_id: uuid.UUID
    quantity: int = Field(..., gt=0, example=6)

class AssetHierarchyCreate(AssetHierarchyBase):
    pass

class AssetHierarchyRead(AssetHierarchyBase):
    class Config:
        from_attributes = True


# --- Esquemas Compuestos para Respuestas de API Complejas ---

class AssetTypeWithHierarchy(AssetTypeRead):
    # Muestra los componentes directos de un tipo de activo
    children: List[AssetHierarchyRead] = []
    # Muestra de qué activos más grandes es componente
    parents: List[AssetHierarchyRead] = []
