# /app/configuration/schemas.py
"""
Esquemas Pydantic para el módulo de Configuración.
"""
import uuid
from typing import Optional, List
from pydantic import BaseModel, Field

# --- ConfigurationParameter ---

class ConfigurationParameterBase(BaseModel):
    key: str = Field(..., min_length=3, max_length=100, example="SMTP_HOST")
    value: str = Field(..., example="smtp.gmail.com")
    description: Optional[str] = None
    is_editable: bool = True

class ConfigurationParameterCreate(ConfigurationParameterBase):
    pass

class ConfigurationParameterUpdate(BaseModel):
    value: str

class ConfigurationParameterRead(ConfigurationParameterBase):
    id: uuid.UUID
    
    class Config:
        from_attributes = True

# --- EnumType y EnumValue ---

class EnumValueBase(BaseModel):
    value: str = Field(..., example="HIGH")
    label: str = Field(..., example="Alta Prioridad")
    is_active: bool = True
    order: int = 0

class EnumValueCreate(EnumValueBase):
    pass

class EnumValueRead(EnumValueBase):
    id: uuid.UUID
    
    class Config:
        from_attributes = True

class EnumTypeBase(BaseModel):
    name: str = Field(..., example="WorkOrderPriority")
    description: Optional[str] = None

class EnumTypeRead(EnumTypeBase):
    id: uuid.UUID
    values: List[EnumValueRead] = []

    class Config:
        from_attributes = True
