# /app/notifications/schemas.py
"""
Esquemas Pydantic para el Módulo de Notificaciones.
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .models import NotificationLevel

class NotificationBase(BaseModel):
    level: NotificationLevel
    icon: Optional[str] = None
    title: str
    message: str
    action_url: Optional[str] = None

class NotificationCreate(NotificationBase):
    recipient_id: uuid.UUID
    tenant_id: Optional[uuid.UUID] = None

class NotificationRead(NotificationBase):
    id: uuid.UUID
    recipient_id: uuid.UUID
    tenant_id: Optional[uuid.UUID]
    read_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class MarkAsReadResponse(BaseModel):
    updated: int
