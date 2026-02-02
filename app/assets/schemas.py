# /app/assets/schemas.py
"""
Esquemas Pydantic para el módulo de Activos (Assets), alineados con el contrato de API.
"""
import uuid
from datetime import date, datetime
from typing import Optional, List, Any, Dict

from pydantic import BaseModel, Field

from app.sectors.schemas import SectorRead


# --- Esquemas para AssetType (El Catálogo) ---
class AssetTypeBase(BaseModel):
    name: str = Field(..., example="Servo Motor X5")
    description: Optional[str] = Field(None, example="Motor de alta precisión para brazos robóticos.")
    category: Optional[str] = Field(None, example="MOTOR", description="MACHINE, SENSOR, PLC, AREA, etc.")

class AssetTypeCreate(AssetTypeBase):
    pass

class AssetTypeRead(AssetTypeBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


# --- Esquemas para Asset (La Instancia Física) ---

class AssetCreate(BaseModel):
    asset_type_id: uuid.UUID
    sector_id: Optional[uuid.UUID] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None

class AssetUpdate(BaseModel):
    """Esquema para actualizar una instancia de activo existente."""
    sector_id: Optional[uuid.UUID] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    last_maintenance_at: Optional[date] = None
    warranty_expires_at: Optional[date] = None

class AssetStatusUpdate(BaseModel):
    status: str = Field(..., example="MAINTENANCE")


# --- DTO Principal para la API, alineado con `assets-api.md` ---

class AssetReadDTO(BaseModel):
    id: uuid.UUID = Field(..., alias="uuid")
    is_active: bool = Field(..., alias="isActive")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    name: str
    description: Optional[str] = None
    type: Optional[str] = None
    status: str
    properties: Optional[Dict[str, Any]] = None
    sector: Optional[SectorRead] = None
    parent_id: Optional[uuid.UUID] = Field(None, alias="parentId")

    class Config:
        from_attributes = True
        populate_by_name = True


# --- Esquemas para AssetHierarchy ---

class AssetHierarchyCreate(BaseModel):
    parent_asset_type_id: uuid.UUID
    child_asset_type_id: uuid.UUID
    quantity: int = Field(..., gt=0)
