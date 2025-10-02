# /app/notifications/models/notification.py
"""
Modelo de la base de datos para la entidad Notification.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Notification(Base):
    """Modelo SQLAlchemy para una Notificación de usuario."""
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relación con el usuario que recibe la notificación
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User")

    # Contenido y estado
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    message = Column(String(500), nullable=False)
    
    # Contexto de la notificación
    type = Column(String(50), nullable=False, index=True, comment="Ej: ALARM, MAINTENANCE_ASSIGNMENT")
    reference_id = Column(String(255), nullable=False, index=True, comment="El UUID de la alarma o la orden de trabajo relacionada")
