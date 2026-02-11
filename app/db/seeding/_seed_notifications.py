# /app/db/seeding/_seed_notifications.py
"""
Seeder para la configuración inicial del módulo de notificaciones.
"""
import logging
from sqlalchemy.orm import Session

from app.notifications.models import (
    NotificationChannel, NotificationTemplate, NotificationRule, 
    NotificationChannelType, NotificationRecipientType, NotificationLevel
)
from app.identity.models import Role

logger = logging.getLogger(__name__)

async def seed_notifications(db: Session, context: dict):
    logger.info("--- [X/9] Poblando Configuración de Notificaciones ---")
    
    # Recuperar roles del contexto (o buscarlos si no están)
    global_roles = context.get("global_roles")
    if not global_roles:
        platform_admin_role = db.query(Role).filter(Role.name == "PLATFORM_ADMIN").first()
    else:
        platform_admin_role = global_roles.get("PLATFORM_ADMIN")

    if not platform_admin_role:
        logger.warning("⚠️ No se encontró el rol PLATFORM_ADMIN. Saltando seed de notificaciones.")
        return

    # 1. Canal IN_APP
    channel = db.query(NotificationChannel).filter(NotificationChannel.type == NotificationChannelType.IN_APP).first()
    if not channel:
        channel = NotificationChannel(
            name="In-App Notifications",
            type=NotificationChannelType.IN_APP,
            is_active=True
        )
        db.add(channel)
        db.commit()
        logger.info("✅ Canal de notificación creado: IN_APP")

    # 2. Plantilla de Borrado de Tenant
    template_name = "TENANT_DELETION_REQUEST"
    template = db.query(NotificationTemplate).filter(NotificationTemplate.name == template_name).first()
    if not template:
        template = NotificationTemplate(
            name=template_name,
            description="Notificación para solicitar aprobación de borrado de tenant",
            level=NotificationLevel.PLATFORM,
            subject="Solicitud de Borrado: {{ tenant_name }}",
            body="El usuario {{ requester_name }} ha solicitado eliminar el tenant '{{ tenant_name }}'. Justificación: {{ justification }}. Se requiere su aprobación.",
            placeholders={"tenant_name": "Nombre del tenant", "requester_name": "Usuario solicitante", "justification": "Motivo"}
        )
        db.add(template)
        db.commit()
        logger.info(f"✅ Plantilla creada: {template_name}")

    # 3. Regla de Notificación
    rule_name = "NotifyPlatformAdminsOnTenantDeletion"
    if not db.query(NotificationRule).filter(NotificationRule.name == rule_name).first():
        rule = NotificationRule(
            name=rule_name,
            event_type="saas:tenant_deletion_requested",
            template_id=template.id,
            channel_id=channel.id,
            recipient_type=NotificationRecipientType.ROLE,
            recipient_id=platform_admin_role.id,
            is_active=True
        )
        db.add(rule)
        db.commit()
        logger.info(f"✅ Regla creada: {rule_name}")
