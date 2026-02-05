# /app/alarming/schemas.py
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# --- Esquemas para AlarmRule ---

class AlarmRuleBase(BaseModel):
    asset_id: uuid.UUID
    metric_name: str
    condition: str
    threshold: float
    severity: str = "warning"
    is_enabled: bool = True

class AlarmRuleCreate(AlarmRuleBase):
    pass

class AlarmRuleUpdate(BaseModel):
    metric_name: Optional[str] = None
    condition: Optional[str] = None
    threshold: Optional[float] = None
    severity: Optional[str] = None
    is_enabled: Optional[bool] = None

class AlarmRule(AlarmRuleBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

# --- Esquemas para Alarm ---

class AlarmBase(BaseModel):
    rule_id: uuid.UUID
    triggering_value: float
    is_acknowledged: bool

class AlarmCreate(AlarmBase):
    pass

class AlarmRead(AlarmBase): # Renombrado de Alarm a AlarmRead
    id: uuid.UUID
    created_at: datetime
    rule: AlarmRule # Anidar la regla para tener contexto

    class Config:
        from_attributes = True
