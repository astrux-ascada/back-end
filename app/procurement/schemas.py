# /app/procurement/schemas.py
"""
Esquemas Pydantic para el módulo de Compras (Procurement).

Define los contratos de datos para la API, empezando por la entidad Provider.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# --- Esquemas para Provider ---

class ProviderBase(BaseModel):
    name: str = Field(..., example="Soluciones Industriales ACME")
    contact_info: Optional[str] = Field(None, example="contact@acme.com, +34 912 345 678")
    specialty: Optional[str] = Field(None, example="Robótica y Automatización")
    performance_score: Optional[float] = Field(None, ge=0, le=100, example=95.5)

class ProviderCreate(ProviderBase):
    pass

class ProviderRead(ProviderBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
