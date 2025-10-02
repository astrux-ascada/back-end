# /app/configuration/schemas.py
"""
Esquemas Pydantic para el módulo de Configuración.
"""
import uuid
from typing import Optional, List

from pydantic import BaseModel, Field


# --- Esquemas para ConfigurationParameter ---

class ConfigurationParameterBase(BaseModel):
    value: str

class ConfigurationParameterUpdate(ConfigurationParameterBase):
    pass

class ConfigurationParameterRead(ConfigurationParameterBase):
    key: str
    description: Optional[str] = None
    is_editable: bool = Field(..., alias="isEditable")

    class Config:
        from_attributes = True
        populate_by_name = True


# --- Esquemas para EnumValue ---

class EnumValueBase(BaseModel):
    value: str = Field(..., example="IN_PROGRESS")
    label: str = Field(..., example="En Progreso")
    color: Optional[str] = Field(None, example="#3b82f6")

class EnumValueCreate(EnumValueBase):
    pass

class EnumValueRead(EnumValueBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


# --- Esquemas para EnumType ---

class EnumTypeBase(BaseModel):
    name: str = Field(..., example="WorkOrderStatus")
    description: Optional[str] = None

class EnumTypeCreate(EnumTypeBase):
    pass

class EnumTypeRead(EnumTypeBase):
    id: uuid.UUID
    values: List[EnumValueRead] = []

    class Config:
        from_attributes = True
