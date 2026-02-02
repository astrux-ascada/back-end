# /app/notifications/schemas.py
"""
Esquemas Pydantic para el módulo de Notificaciones.
"""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class Notification(BaseModel):
    id: uuid.UUID = Field(..., alias="uuid")
    created_at: datetime = Field(..., alias="createdAt")
    is_read: bool = Field(..., alias="isRead")
    message: str
    type: str
    reference_id: str = Field(..., alias="referenceId")

    class Config:
        from_attributes = True
        populate_by_name = True
