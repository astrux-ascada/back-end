# /app/notifications/service.py
"""
Capa de Servicio para el módulo de Notificaciones.
"""
import logging
from typing import List
import uuid
from sqlalchemy.orm import Session

from app.notifications import models, schemas
from app.core.event_broker import EventBroker

logger = logging.getLogger("app.notifications.service")

class NotificationService:
    """Servicio de negocio para la gestión de notificaciones."""

    def __init__(self, db: Session, event_broker: EventBroker):
        self.db = db
        self.event_broker = event_broker
        # Suscribirse a los eventos relevantes al iniciar el servicio
        self._subscribe_to_events()

    def _subscribe_to_events(self):
        """Define las suscripciones a eventos del sistema."""
        self.event_broker.subscribe("alarm:triggered", self._handle_alarm_triggered)
        # Aquí se podrían añadir más suscripciones, ej:
        # self.event_broker.subscribe("maintenance:completed", self._handle_maintenance_completed)

    def _handle_alarm_triggered(self, event_data: dict):
        """
        Manejador para el evento 'alarm:triggered'.
        Crea una notificación en la base de datos.
        """
        logger.info(f"Evento 'alarm:triggered' recibido: {event_data}")
        
        notification_in = schemas.NotificationCreate(
            user_id=event_data["user_id"], # Asumiendo que el evento contiene el user_id
            type="ALARM",
            content=event_data["content"],
            reference_id=event_data["alarm_id"]
        )
        self.create_notification(notification_in)

    def create_notification(self, notification_in: schemas.NotificationCreate) -> models.Notification:
        """Crea una nueva notificación en la base de datos."""
        db_notification = models.Notification(
            user_id=notification_in.user_id,
            type=notification_in.type,
            content=notification_in.content,
            reference_id=notification_in.reference_id
        )
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)
        logger.info(f"Notificación creada para el usuario {db_notification.user_id}")
        return db_notification

    def get_notifications_for_user(self, user_id: uuid.UUID) -> List[models.Notification]:
        """Obtiene todas las notificaciones no leídas para un usuario."""
        return self.db.query(models.Notification).filter(
            models.Notification.user_id == user_id,
            models.Notification.is_read == False
        ).order_by(models.Notification.created_at.desc()).all()

    def mark_as_read(self, notification_id: uuid.UUID, user_id: uuid.UUID) -> models.Notification:
        """Marca una notificación como leída."""
        db_notification = self.db.query(models.Notification).filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == user_id
        ).first()
        
        if db_notification:
            db_notification.is_read = True
            self.db.commit()
            self.db.refresh(db_notification)
        
        return db_notification
