# /app/notifications/schemas.py
"""
Esquemas Pydantic para el módulo de Notificaciones.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

# --- Esquemas para Notificaciones ---

class NotificationBase(BaseModel):
    user_id: uuid.UUID
    type: str
    content: str
    reference_id: str

class NotificationCreate(NotificationBase):
    pass

class NotificationRead(NotificationBase):
    id: uuid.UUID
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
