# /app/sectors/schemas.py
"""
Esquemas Pydantic para el módulo de Sectores.
"""
import uuid
from typing import Optional, List
from pydantic import BaseModel, Field

class SectorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None

class SectorCreate(SectorBase):
    pass

class SectorUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None

class SectorRead(SectorBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    # Para evitar recursión infinita en la respuesta, no incluimos 'children' aquí por defecto,
    # o usamos un esquema simplificado si fuera necesario.
    
    class Config:
        from_attributes = True

# Esquema para árbol de sectores (opcional, para vistas jerárquicas)
class SectorTree(SectorRead):
    children: List['SectorTree'] = []
