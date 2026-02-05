# /app/procurement/schemas.py
"""
Esquemas Pydantic para el módulo de Compras (Procurement).
"""
import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# --- Esquemas para SparePart ---

class SparePartBase(BaseModel):
    name: str = Field(..., example="Rodamiento de bolas 6204-2RS")
    description: Optional[str] = Field(None, example="Rodamiento rígido de una hilera de bolas, sellado.")
    part_number: Optional[str] = Field(None, example="SKF-6204-2RS")
    current_stock: int = Field(0, ge=0)
    min_stock_level: int = Field(0, ge=0)
    unit_cost: float = Field(0.0, ge=0)
    provider_id: Optional[uuid.UUID] = None

class SparePartCreate(SparePartBase):
    pass

class SparePartUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    part_number: Optional[str] = None
    current_stock: Optional[int] = Field(None, ge=0)
    min_stock_level: Optional[int] = Field(None, ge=0)
    unit_cost: Optional[float] = Field(None, ge=0)
    provider_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = None

class SparePartRead(SparePartBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Esquemas para Provider ---

class ProviderBase(BaseModel):
    name: str = Field(..., example="Soluciones Industriales ACME")
    contact_info: Optional[str] = Field(None, example="contact@acme.com, +34 912 345 678")
    specialty: Optional[str] = Field(None, example="Robótica y Automatización")
    performance_score: Optional[float] = Field(None, ge=0, le=100, example=95.5)

class ProviderCreate(ProviderBase):
    pass

class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None
    specialty: Optional[str] = None
    performance_score: Optional[float] = Field(None, ge=0, le=100)

class ProviderRead(ProviderBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Incluir los repuestos que ofrece este proveedor
    spare_parts: List[SparePartRead] = []

    class Config:
        from_attributes = True


# --- Esquemas para SparePart ---

class SparePartBase(BaseModel):
    name: str = Field(..., example="Rodamiento de Bolas 6203-2RS")
    part_number: str = Field(..., example="SKF-6203-2RS")
    price: Optional[float] = Field(None, example=15.75)

class SparePartCreate(SparePartBase):
    stock_quantity: int = Field(0, description="Cantidad inicial en stock al crear el repuesto.")

class SparePartUpdate(BaseModel):
    name: Optional[str] = None
    part_number: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None # Permitir ajuste manual de stock (aunque idealmente debería ser por movimientos)

class SparePartRead(SparePartBase):
    id: uuid.UUID
    stock_quantity: int

    class Config:
        from_attributes = True
