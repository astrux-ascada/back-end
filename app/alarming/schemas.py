# /app/alarming/schemas.py
"""
Esquemas Pydantic para el módulo de Alertas.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

# --- Esquemas para AlarmRule ---

class AlarmRuleBase(BaseModel):
    asset_id: uuid.UUID = Field(..., alias="assetId")
    metric_name: str = Field(..., example="temperature_celsius", alias="metricName")
    condition: str = Field(..., example=">")
    threshold: float
    severity: str = Field(..., example="CRITICAL")
    is_enabled: bool = Field(True, alias="isEnabled")

class AlarmRuleCreate(AlarmRuleBase):
    pass

class AlarmRuleRead(AlarmRuleBase):
    id: uuid.UUID = Field(..., alias="uuid")

    class Config:
        from_attributes = True
        populate_by_name = True


# --- Esquemas para Alarm ---

class AlarmBase(BaseModel):
    status: str = Field(..., example="ACTIVE")
    triggering_value: float = Field(..., alias="triggeringValue")

class AlarmRead(AlarmBase):
    id: uuid.UUID = Field(..., alias="uuid")
    triggered_at: datetime = Field(..., alias="triggeredAt")
    acknowledged_at: Optional[datetime] = Field(None, alias="acknowledgedAt")
    cleared_at: Optional[datetime] = Field(None, alias="clearedAt")
    rule: AlarmRuleRead

    class Config:
        from_attributes = True
        populate_by_name = True
