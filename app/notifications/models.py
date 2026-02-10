# /app/notifications/models.py
"""
Modelos de base de datos para el Módulo de Notificaciones.
"""
import uuid
from sqlalchemy import Column, String, Text, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base

class NotificationLevel(str, enum.Enum):
    TENANT = "TENANT"
    PLATFORM = "PLATFORM"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    recipient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True, index=True)
    
    level = Column(SQLAlchemyEnum(NotificationLevel, name="notification_level"), nullable=False)
    
    icon = Column(String(50), nullable=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    action_url = Column(Text, nullable=True)
    
    read_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default="NOW()", nullable=False)

    recipient = relationship("User")
    tenant = relationship("Tenant")
