# /app/notifications/api.py
"""
API Router para el módulo de Notificaciones.
"""
import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from app.notifications import schemas
from app.notifications.service import NotificationService
from app.dependencies.services import get_notification_service
from app.dependencies.auth import get_current_active_user
from app.identity.models import User

logger = logging.getLogger("app.notifications.api")

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=List[schemas.NotificationRead])
def get_my_notifications(
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene todas las notificaciones no leídas para el usuario autenticado.
    """
    return notification_service.get_notifications_for_user(current_user.id)

@router.post("/{notification_id}/read", response_model=schemas.NotificationRead)
def mark_notification_as_read(
    notification_id: uuid.UUID,
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Marca una notificación específica como leída.
    """
    notification = notification_service.mark_as_read(notification_id, current_user.id)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificación no encontrada.")
    return notification
