# /app/notifications/service.py
"""
Capa de Servicio para el Módulo de Notificaciones.
"""
import uuid
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from . import models, schemas
from app.identity.models import User, Role

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def process_event(self, event_type: str, event_data: Dict[str, Any]):
        """
        Procesa un evento, busca reglas coincidentes y despacha notificaciones.
        """
        logger.info(f"Procesando evento de notificación: {event_type}")
        rules = self.db.query(models.NotificationRule).filter(
            models.NotificationRule.event_type == event_type,
            models.NotificationRule.is_active == True
        ).all()

        if not rules:
            logger.warning(f"No se encontraron reglas activas para el evento: {event_type}")
            return

        for rule in rules:
            try:
                self._dispatch_notification_for_rule(rule, event_data)
            except Exception as e:
                logger.error(f"Error al procesar la regla '{rule.name}' para el evento '{event_type}': {e}", exc_info=True)

    def _dispatch_notification_for_rule(self, rule: models.NotificationRule, event_data: Dict[str, Any]):
        """
        (Método interno) Despacha una notificación para una regla y evento específicos.
        """
        # 1. Renderizar la plantilla
        title = self._render_template(rule.template.subject or rule.template.name, event_data)
        message = self._render_template(rule.template.body, event_data)
        action_url = self._render_template(rule.template.action_url, event_data) if rule.template.action_url else None

        # 2. Determinar los destinatarios
        recipients = self._get_recipients_for_rule(rule, event_data)

        # 3. Despachar por canal
        if rule.channel.type == models.NotificationChannelType.IN_APP:
            self._send_in_app_notifications(recipients, rule.template.level, title, message, action_url)
        elif rule.channel.type == models.NotificationChannelType.EMAIL:
            # Lógica para enviar email (futuro)
            logger.info(f"CANAL EMAIL (futuro): Enviando a {len(recipients)} destinatarios. Título: {title}")
            pass
        # ... otros canales

    def _render_template(self, template_string: str, data: Dict[str, Any]) -> str:
        """
        (Método interno) Reemplaza placeholders como {{ key }} con valores de los datos del evento.
        """
        for key, value in data.items():
            template_string = template_string.replace(f"{{{{ {key} }}}}", str(value))
        return template_string

    def _get_recipients_for_rule(self, rule: models.NotificationRule, event_data: Dict[str, Any]) -> List[User]:
        """
        (Método interno) Obtiene la lista de usuarios destinatarios según la regla.
        """
        recipient_type = rule.recipient_type
        
        if recipient_type == models.NotificationRecipientType.ROLE:
            return self.db.query(User).join(User.roles).filter(Role.id == rule.recipient_id).all()
        
        if recipient_type == models.NotificationRecipientType.USER:
            user = self.db.query(User).filter(User.id == rule.recipient_id).first()
            return [user] if user else []
            
        if recipient_type == models.NotificationRecipientType.REQUESTER:
            requester_id = event_data.get("requester_id")
            if requester_id:
                user = self.db.query(User).filter(User.id == requester_id).first()
                return [user] if user else []
        
        # TODO: Implementar lógica para TENANT_ADMIN_OF_ENTITY
        
        return []

    def _send_in_app_notifications(self, recipients: List[User], level: models.NotificationLevel, title: str, message: str, action_url: str = None):
        """
        (Método interno) Crea notificaciones IN_APP en la base de datos.
        """
        notifications_to_create = []
        for user in recipients:
            notif_in = schemas.NotificationCreate(
                recipient_id=user.id,
                tenant_id=user.tenant_id if level == models.NotificationLevel.TENANT else None,
                level=level,
                title=title,
                message=message,
                action_url=action_url
            )
            notifications_to_create.append(models.Notification(**notif_in.model_dump()))

        if notifications_to_create:
            self.db.add_all(notifications_to_create)
            self.db.commit()
            logger.info(f"Creadas {len(notifications_to_create)} notificaciones IN_APP.")

    # --- Métodos existentes para la API (lectura, etc.) ---

    def get_notifications_for_user(self, user_id: uuid.UUID, unread_only: bool = True, limit: int = 20) -> List[models.Notification]:
        query = self.db.query(models.Notification).filter(models.Notification.recipient_id == user_id)
        if unread_only:
            query = query.filter(models.Notification.read_at == None)
        return query.order_by(models.Notification.created_at.desc()).limit(limit).all()

    def mark_as_read(self, notification_id: uuid.UUID, user_id: uuid.UUID) -> models.Notification:
        notification = self.db.query(models.Notification).filter(models.Notification.id == notification_id, models.Notification.recipient_id == user_id).first()
        if notification and not notification.read_at:
            notification.read_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(notification)
        return notification

    def mark_all_as_read(self, user_id: uuid.UUID) -> int:
        result = self.db.query(models.Notification).filter(models.Notification.recipient_id == user_id, models.Notification.read_at == None).update({"read_at": datetime.utcnow()})
        self.db.commit()
        return result
