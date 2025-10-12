# /app/notifications/service.py
"""
Capa de Servicio para el módulo de Notificaciones.
"""

import logging
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from app.notifications import models, schemas
from app.notifications.repository import NotificationRepository
from app.identity.models import User

logger = logging.getLogger(__name__)


class NotificationService:
    """Servicio de negocio para la gestión de notificaciones de usuario."""

    def __init__(self, db: Session):
        self.db = db
        self.notification_repo = NotificationRepository(self.db)

    def create_notification_for_user(
        self, 
        user_id: uuid.UUID, 
        message: str, 
        type: str, 
        reference_id: str
    ) -> models.Notification:
        """Crea y guarda una notificación para un usuario específico."""
        # Lógica futura: Aquí se podría integrar con servicios de envío de email o push notifications.
        logger.info(f"Creando notificación para el usuario {user_id}: {message}")
        return self.notification_repo.create_notification(user_id, message, type, reference_id)

    def get_notifications(self, user: User, include_read: bool) -> List[models.Notification]:
        """Obtiene las notificaciones para el usuario actual."""
        return self.notification_repo.get_notifications_for_user(user.id, include_read)

    def mark_notification_as_read(self, notification_id: uuid.UUID, user: User) -> Optional[models.Notification]:
        """Marca una notificación como leída para el usuario actual."""
        return self.notification_repo.mark_as_read(notification_id, user.id)

    def mark_all_notifications_as_read(self, user: User) -> int:
        """Marca todas las notificaciones de un usuario como leídas."""
        return self.notification_repo.mark_all_as_read(user.id)
