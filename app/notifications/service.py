# /app/notifications/service.py
"""
Capa de Servicio para el Módulo de Notificaciones.
"""
import uuid
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from .models import Notification
from .schemas import NotificationCreate
from app.identity.models import User, Role

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, notif_in: NotificationCreate) -> Notification:
        """
        Crea una única notificación para un destinatario específico.
        """
        db_notif = Notification(**notif_in.model_dump())
        self.db.add(db_notif)
        self.db.commit()
        self.db.refresh(db_notif)
        return db_notif

    def create_platform_notification_for_role(
        self,
        role_name: str,
        title: str,
        message: str,
        icon: str = "bell",
        action_url: str = None
    ) -> List[Notification]:
        """
        Crea una notificación para todos los usuarios con un rol específico a nivel de plataforma.
        """
        users_with_role = self.db.query(User).join(User.roles).filter(Role.name == role_name).all()
        
        notifications = []
        for user in users_with_role:
            notif_in = NotificationCreate(
                recipient_id=user.id,
                level="PLATFORM",
                icon=icon,
                title=title,
                message=message,
                action_url=action_url
            )
            notifications.append(Notification(**notif_in.model_dump()))

        if notifications:
            self.db.add_all(notifications)
            self.db.commit()
        
        return notifications

    def get_notifications_for_user(
        self, 
        user_id: uuid.UUID, 
        unread_only: bool = True, 
        limit: int = 20
    ) -> List[Notification]:
        """
        Obtiene las notificaciones para un usuario.
        """
        query = self.db.query(Notification).filter(Notification.recipient_id == user_id)
        if unread_only:
            query = query.filter(Notification.read_at == None)
        
        return query.order_by(Notification.created_at.desc()).limit(limit).all()

    def mark_as_read(self, notification_id: uuid.UUID, user_id: uuid.UUID) -> Notification:
        """
        Marca una notificación específica como leída.
        """
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.recipient_id == user_id
        ).first()

        if notification and not notification.read_at:
            notification.read_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(notification)
        
        return notification

    def mark_all_as_read(self, user_id: uuid.UUID) -> int:
        """
        Marca todas las notificaciones de un usuario como leídas.
        """
        result = self.db.query(Notification).filter(
            Notification.recipient_id == user_id,
            Notification.read_at == None
        ).update({"read_at": datetime.utcnow()})
        
        self.db.commit()
        return result
