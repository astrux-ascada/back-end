# /app/core_engine/schemas.py
"""
Esquemas Pydantic para el módulo Core Engine.

Define los contratos de datos para la API, empezando por la entidad DataSource.
"""
import uuid
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field, Json


# --- Esquemas para DataSource ---

class DataSourceBase(BaseModel):
    name: str = Field(..., example="PLC Línea de Ensamblaje 3")
    protocol: str = Field(..., example="OPCUA")
    connection_params: Json[Any] = Field(..., example='{"host": "192.168.1.10", "port": 4840}')
    is_active: bool = Field(False, description="Habilita o deshabilita la recolección de datos.")
    description: Optional[str] = Field(None, example="Controlador principal del brazo robótico de soldadura.")

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceRead(DataSourceBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
