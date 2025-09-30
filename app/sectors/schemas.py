# /app/sectors/schemas.py
"""
Esquemas Pydantic para el módulo de Sectores.
"""
import uuid
from typing import Optional

from pydantic import BaseModel, Field


class SectorBase(BaseModel):
    name: str = Field(..., example="Línea de Ensamblaje 1")
    description: Optional[str] = Field(None, example="Sector de ensamblaje de chasis.")

class SectorCreate(SectorBase):
    pass

class SectorRead(BaseModel):
    id: uuid.UUID = Field(..., alias="uuid")
    name: str

    class Config:
        from_attributes = True
        populate_by_name = True
