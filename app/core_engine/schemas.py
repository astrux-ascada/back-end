# /app/core_engine/schemas.py
"""
Esquemas Pydantic para el Core Engine.
"""
import uuid
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Esquemas para DataSource ---

class DataSourceBase(BaseModel):
    name: str = Field(..., example="PLC Línea 1")
    protocol: str = Field(..., example="modbus_tcp")
    connection_params: Dict[str, Any] = Field(..., example={"host": "192.168.1.10", "port": 502})
    is_active: bool = True

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceUpdate(BaseModel):
    name: Optional[str] = None
    protocol: Optional[str] = None
    connection_params: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class DataSourceRead(DataSourceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID

    class Config:
        from_attributes = True
