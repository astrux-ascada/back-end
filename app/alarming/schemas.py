# /app/alarming/schemas.py
import uuid
from pydantic import BaseModel, Field

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
