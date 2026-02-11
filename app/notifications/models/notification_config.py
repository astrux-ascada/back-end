# /app/notifications/models/notification_config.py
"""
Modelos de base de datos para la configuración del Módulo de Notificaciones.
"""
import uuid
from sqlalchemy import Column, String, Text, DateTime, Enum as SQLAlchemyEnum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base

# --- Enumeraciones ---
class NotificationChannelType(str, enum.Enum):
    IN_APP = "IN_APP"
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH" # Notificaciones push a dispositivos móviles/web

class NotificationRecipientType(str, enum.Enum):
    ROLE = "ROLE" # Destinatario es un rol específico (ej: PLATFORM_ADMIN)
    USER = "USER" # Destinatario es un usuario específico
    TENANT_ADMIN_OF_ENTITY = "TENANT_ADMIN_OF_ENTITY" # Admin del tenant al que pertenece la entidad del evento
    REQUESTER = "REQUESTER" # El usuario que inició la acción que generó el evento

# --- Modelos ---

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True) # Ej: "TENANT_DELETION_REQUEST"
    description = Column(Text, nullable=True)
    level = Column(SQLAlchemyEnum("TENANT", "PLATFORM", name="notification_level"), nullable=False) # Reutiliza el ENUM de Notification
    subject = Column(String(255), nullable=True) # Para canales como email
    body = Column(Text, nullable=False) # Contenido de la plantilla con placeholders (ej: "Hola {{ user_name }}, ...")
    placeholders = Column(JSONB, nullable=True, default={}) # Documentación de placeholders esperados
    
    created_at = Column(DateTime(timezone=True), server_default="NOW()", nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default="NOW()", onupdate="NOW()", nullable=False)

class NotificationChannel(Base):
    __tablename__ = "notification_channels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True) # Ej: "In-App Notifications", "Transactional Email"
    type = Column(SQLAlchemyEnum(NotificationChannelType, name="notification_channel_type"), nullable=False)
    config = Column(JSONB, nullable=True, default={}) # Configuración específica del canal (ej: SMTP server, API keys)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default="NOW()", nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default="NOW()", onupdate="NOW()", nullable=False)

class NotificationRule(Base):
    __tablename__ = "notification_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True) # Ej: "NotifyPlatformAdminsOnTenantDeletion"
    event_type = Column(String(100), nullable=False, index=True) # Ej: "saas:tenant_deletion_requested", "alarming:critical_alarm"
    
    template_id = Column(UUID(as_uuid=True), ForeignKey("notification_templates.id"), nullable=False)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("notification_channels.id"), nullable=False)
    
    recipient_type = Column(SQLAlchemyEnum(NotificationRecipientType, name="notification_recipient_type"), nullable=False)
    recipient_id = Column(UUID(as_uuid=True), nullable=True) # ID del rol o usuario, si aplica
    
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default="NOW()", nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default="NOW()", onupdate="NOW()", nullable=False)

    template = relationship("NotificationTemplate")
    channel = relationship("NotificationChannel")
    # No se define relación directa con User/Role aquí para evitar dependencias circulares complejas
    # La resolución del destinatario se hará en la lógica del servicio.
