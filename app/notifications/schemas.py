# /app/notifications/schemas.py
"""
Esquemas Pydantic para el Módulo de Notificaciones.
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from .models import NotificationLevel, NotificationChannelType, NotificationRecipientType

# --- Esquemas para Notificaciones (Instancias) ---

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

# --- Esquemas para Configuración de Notificaciones ---

# --- NotificationTemplate ---
class NotificationTemplateBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    level: NotificationLevel
    subject: Optional[str] = Field(None, max_length=255)
    body: str
    placeholders: Optional[Dict[str, str]] = Field(None, description="Ej: {'user_name': 'Nombre del usuario'}")

class NotificationTemplateCreate(NotificationTemplateBase):
    pass

class NotificationTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    level: Optional[NotificationLevel] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    placeholders: Optional[Dict[str, str]] = None

class NotificationTemplateRead(NotificationTemplateBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- NotificationChannel ---
class NotificationChannelBase(BaseModel):
    name: str = Field(..., max_length=100)
    type: NotificationChannelType
    config: Optional[Dict[str, Any]] = None
    is_active: bool = True

class NotificationChannelCreate(NotificationChannelBase):
    pass

class NotificationChannelUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[NotificationChannelType] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class NotificationChannelRead(NotificationChannelBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- NotificationRule ---
class NotificationRuleBase(BaseModel):
    name: str = Field(..., max_length=100)
    event_type: str = Field(..., max_length=100)
    template_id: uuid.UUID
    channel_id: uuid.UUID
    recipient_type: NotificationRecipientType
    recipient_id: Optional[uuid.UUID] = None # ID del rol o usuario, si aplica
    is_active: bool = True

class NotificationRuleCreate(NotificationRuleBase):
    pass

class NotificationRuleUpdate(BaseModel):
    name: Optional[str] = None
    event_type: Optional[str] = None
    template_id: Optional[uuid.UUID] = None
    channel_id: Optional[uuid.UUID] = None
    recipient_type: Optional[NotificationRecipientType] = None
    recipient_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = None

class NotificationRuleRead(NotificationRuleBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
