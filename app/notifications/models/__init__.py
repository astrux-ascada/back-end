# /app/notifications/models/__init__.py
from .notification import Notification, NotificationLevel
from .notification_config import (
    NotificationTemplate,
    NotificationChannel,
    NotificationRule,
    NotificationChannelType,
    NotificationRecipientType
)
