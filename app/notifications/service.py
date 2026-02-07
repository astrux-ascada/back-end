# /app/notifications/service.py
"""
Capa de Servicio para el módulo de Notificaciones.
"""
import logging
from typing import List
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from app.notifications import models, schemas
from app.core.event_broker import EventBroker
from app.core.email import email_sender # Importar el servicio de email
from app.identity.models import User
from app.identity.models.saas.tenant import Tenant
from app.core.config import settings

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
        Crea una notificación en la base de datos y envía un email.
        """
        logger.info(f"Evento 'alarm:triggered' recibido: {event_data}")
        
        user_id = event_data.get("user_id")
        if not user_id:
            logger.warning("Evento de alarma sin user_id, no se puede notificar.")
            return

        # 1. Crear notificación in-app
        notification_in = schemas.NotificationCreate(
            user_id=user_id,
            type="ALARM",
            content=event_data["content"],
            reference_id=event_data["alarm_id"]
        )
        self.create_notification(notification_in)

        # 2. Enviar Email (Centralización de Comunicaciones)
        self._send_alarm_email(user_id, event_data)

    def _send_alarm_email(self, user_id: uuid.UUID, event_data: dict):
        """Envía un correo de alerta al usuario, personalizado por tenant."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user or not user.email:
                return

            # Obtener datos del tenant para personalización
            tenant_config = {}
            if user.tenant_id:
                tenant = self.db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
                if tenant:
                    tenant_config = {
                        "name": tenant.name,
                        "logo_url": tenant.logo_url,
                        "contact_email": tenant.contact_email,
                        "billing_address": tenant.billing_address
                    }

            # Enviar el correo
            email_sender.send_email(
                to_email=user.email,
                subject=f"🚨 ALERTA: {event_data['content']}",
                template_name="alarm.html", # Necesitaremos crear esta plantilla
                context={
                    "user_name": user.name,
                    "alarm_content": event_data["content"],
                    "year": datetime.now().year,
                    "login_url": f"{settings.BASE_URL}/login"
                },
                tenant_config=tenant_config
            )
        except Exception as e:
            logger.error(f"Error enviando email de alarma: {e}")

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
