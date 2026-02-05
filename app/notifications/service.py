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
from app.identity.repository import UserRepository # Importar para validar tenant

logger = logging.getLogger(__name__)


class NotificationService:
    """Servicio de negocio para la gestión de notificaciones de usuario."""

    def __init__(self, db: Session):
        self.db = db
        self.notification_repo = NotificationRepository(self.db)
        self.user_repo = UserRepository(self.db) # Instanciar repo de usuario

    def create_notification_for_user(
        self, 
        user_id: uuid.UUID, 
        message: str, 
        type: str, 
        reference_id: str
    ) -> Optional[models.Notification]:
        """Crea y guarda una notificación para un usuario específico, validando su tenant."""
        # Obtener el usuario para conseguir su tenant_id
        user = self.user_repo.get_by_id(user_id)
        if not user or not user.tenant_id:
            logger.error(f"Intento de crear notificación para usuario {user_id} sin tenant válido.")
            return None

        logger.info(f"Creando notificación para el usuario {user_id} en el tenant {user.tenant_id}: {message}")
        return self.notification_repo.create_notification(user_id, message, type, reference_id, user.tenant_id)

    def get_notifications(self, user: User, include_read: bool) -> List[models.Notification]:
        """Obtiene las notificaciones para el usuario actual, validando su tenant."""
        if not user.tenant_id:
            return []
        return self.notification_repo.get_notifications_for_user(user.id, user.tenant_id, include_read)

    def mark_notification_as_read(self, notification_id: uuid.UUID, user: User) -> Optional[models.Notification]:
        """Marca una notificación como leída para el usuario actual, validando su tenant."""
        if not user.tenant_id:
            return None
        return self.notification_repo.mark_as_read(notification_id, user.id, user.tenant_id)

    def mark_all_notifications_as_read(self, user: User) -> int:
        """Marca todas las notificaciones de un usuario como leídas, validando su tenant."""
        if not user.tenant_id:
            return 0
        return self.notification_repo.mark_all_as_read(user.id, user.tenant_id)
