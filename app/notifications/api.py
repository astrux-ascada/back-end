# /app/notifications/api.py
"""
API Router para el módulo de Notificaciones.
"""

import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, Response

from app.notifications import schemas
from app.notifications.service import NotificationService
from app.dependencies.services import get_notification_service
from app.dependencies.auth import get_current_active_user
from app.identity.models import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get(
    "/",
    summary="Obtener Notificaciones del Usuario Actual",
    response_model=List[schemas.Notification],
)
def get_notifications(
    include_read: bool = False,
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user),
):
    """Devuelve una lista de las notificaciones del usuario autenticado."""
    return notification_service.get_notifications(current_user, include_read)


@router.post(
    "/{notification_id}/mark-read",
    summary="Marcar una Notificación como Leída",
    response_model=schemas.Notification,
)
def mark_notification_as_read(
    notification_id: uuid.UUID,
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user),
):
    """Marca una notificación específica del usuario actual como leída."""
    return notification_service.mark_notification_as_read(notification_id, current_user)


@router.post(
    "/mark-all-read",
    summary="Marcar Todas las Notificaciones como Leídas",
    status_code=status.HTTP_204_NO_CONTENT,
)
def mark_all_notifications_as_read(
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user),
):
    """Marca todas las notificaciones no leídas del usuario actual como leídas."""
    notification_service.mark_all_notifications_as_read(current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
