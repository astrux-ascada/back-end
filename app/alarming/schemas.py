# /app/alarming/schemas.py
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# --- Alarm Rules ---

class AlarmRuleBase(BaseModel):
    asset_id: uuid.UUID
    metric_name: str
    condition: str
    threshold: float
    severity: str = "warning"
    is_enabled: bool = True

class AlarmRuleCreate(AlarmRuleBase):
    pass

class AlarmRule(AlarmRuleBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

# --- Alarms ---

class AlarmBase(BaseModel):
    alarm_rule_id: uuid.UUID
    asset_id: uuid.UUID
    triggered_value: float
    severity: str

class AlarmRead(AlarmBase):
    id: uuid.UUID
    triggered_at: datetime
    acknowledged: bool
    acknowledged_at: Optional[datetime] = None

    class Config:
        from_attributes = True
