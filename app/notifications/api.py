# /app/notifications/api.py
"""
API Router para el Módulo de Notificaciones.
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_active_user
from app.dependencies.services import get_notification_service
from app.identity.models import User
from .service import NotificationService
from .schemas import NotificationRead, MarkAsReadResponse

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/", response_model=List[NotificationRead])
def get_my_notifications(
    unread_only: bool = True,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    notif_service: NotificationService = Depends(get_notification_service)
):
    """
    Obtiene las notificaciones para el usuario autenticado.
    """
    return notif_service.get_notifications_for_user(current_user.id, unread_only, limit)

@router.post("/{notification_id}/read", response_model=NotificationRead)
def mark_notification_as_read(
    notification_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    notif_service: NotificationService = Depends(get_notification_service)
):
    """
    Marca una notificación específica como leída.
    """
    return notif_service.mark_as_read(notification_id, current_user.id)

@router.post("/read-all", response_model=MarkAsReadResponse)
def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_active_user),
    notif_service: NotificationService = Depends(get_notification_service)
):
    """
    Marca todas las notificaciones del usuario como leídas.
    """
    updated_count = notif_service.mark_all_as_read(current_user.id)
    return {"updated": updated_count}
