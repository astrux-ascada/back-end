# /app/notifications/repository.py
"""
Capa de Repositorio para el módulo de Notificaciones.
"""

from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from app.notifications import models, schemas
from app.identity.models import User # Importar User para el join

class NotificationRepository:
    """Realiza operaciones CRUD para la entidad Notification."""

    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, user_id: uuid.UUID, message: str, type: str, reference_id: str, tenant_id: uuid.UUID) -> models.Notification:
        """Crea un nuevo registro de notificación para un usuario."""
        db_notification = models.Notification(
            user_id=user_id,
            message=message,
            type=type,
            reference_id=reference_id,
            tenant_id=tenant_id
        )
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification

    def get_notifications_for_user(self, user_id: uuid.UUID, tenant_id: uuid.UUID, include_read: bool = False) -> List[models.Notification]:
        """Obtiene las notificaciones de un usuario, validando el tenant."""
        query = self.db.query(models.Notification).join(User).filter(
            models.Notification.user_id == user_id,
            User.tenant_id == tenant_id
        )
        if not include_read:
            query = query.filter(models.Notification.is_read == False)
        return query.order_by(models.Notification.created_at.desc()).all()

    def mark_as_read(self, notification_id: uuid.UUID, user_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.Notification]:
        """Marca una notificación específica como leída, verificando que pertenezca al usuario y al tenant."""
        db_notification = self.db.query(models.Notification).join(User).filter(
            models.Notification.id == notification_id, 
            models.Notification.user_id == user_id,
            User.tenant_id == tenant_id
        ).first()
        
        if db_notification and not db_notification.is_read:
            db_notification.is_read = True
            self.db.commit()
            self.db.refresh(db_notification)
        return db_notification

    def mark_all_as_read(self, user_id: uuid.UUID, tenant_id: uuid.UUID) -> int:
        """Marca todas las notificaciones no leídas de un usuario como leídas, validando el tenant."""
        # Subquery para obtener los IDs de las notificaciones a actualizar
        subquery = self.db.query(models.Notification.id).join(User).filter(
            models.Notification.user_id == user_id,
            User.tenant_id == tenant_id,
            models.Notification.is_read == False
        ).subquery()

        update_query = self.db.query(models.Notification).filter(
            models.Notification.id.in_(subquery)
        )
        updated_count = update_query.update({"is_read": True}, synchronize_session=False)
        self.db.commit()
        return updated_count
