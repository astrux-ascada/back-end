import os
import sys
import logging

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.identity.models import User, Role, Permission
from app.notifications.models import NotificationChannel, NotificationTemplate, NotificationRule, NotificationChannelType, NotificationRecipientType, NotificationLevel
from app.core.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_initial_data():
    db = SessionLocal()
    try:
        logger.info("🌱 Iniciando carga de datos iniciales (Seed)...")

        # 1. Crear Roles Base
        roles = ["GLOBAL_SUPER_ADMIN", "PLATFORM_ADMIN", "TENANT_ADMIN", "OPERATOR"]
        db_roles = {}
        for role_name in roles:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name, description=f"Rol predeterminado {role_name}")
                db.add(role)
                db.flush()
                logger.info(f"✅ Rol creado: {role_name}")
            db_roles[role_name] = role

        # 2. Crear Usuarios
        # 2.1 Super Admin
        super_email = "admin@astruxa.com"
        if not db.query(User).filter(User.email == super_email).first():
            super_user = User(
                email=super_email,
                name="Super Admin",
                hashed_password=hash_password("admin123"), # CORREGIDO
                is_active=True
            )
            super_user.roles.append(db_roles["GLOBAL_SUPER_ADMIN"])
            db.add(super_user)
            logger.info(f"✅ Superusuario creado: {super_email}")

        # 2.2 Platform Admin
        platform_email = "platform@astruxa.com"
        if not db.query(User).filter(User.email == platform_email).first():
            platform_user = User(
                email=platform_email,
                name="Platform Manager",
                hashed_password=hash_password("platform123"), # CORREGIDO
                is_active=True
            )
            platform_user.roles.append(db_roles["PLATFORM_ADMIN"])
            db.add(platform_user)
            logger.info(f"✅ Platform Admin creado: {platform_email}")

        # 3. Configuración de Notificaciones
        # 3.1 Canal IN_APP
        channel = db.query(NotificationChannel).filter(NotificationChannel.type == NotificationChannelType.IN_APP).first()
        if not channel:
            channel = NotificationChannel(
                name="In-App Notifications",
                type=NotificationChannelType.IN_APP,
                is_active=True
            )
            db.add(channel)
            db.flush()
            logger.info("✅ Canal de notificación creado: IN_APP")

        # 3.2 Plantilla de Borrado de Tenant
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
            db.flush()
            logger.info(f"✅ Plantilla creada: {template_name}")

        # 3.3 Regla de Notificación
        rule_name = "NotifyPlatformAdminsOnTenantDeletion"
        if not db.query(NotificationRule).filter(NotificationRule.name == rule_name).first():
            rule = NotificationRule(
                name=rule_name,
                event_type="saas:tenant_deletion_requested",
                template_id=template.id,
                channel_id=channel.id,
                recipient_type=NotificationRecipientType.ROLE,
                recipient_id=db_roles["PLATFORM_ADMIN"].id,
                is_active=True
            )
            db.add(rule)
            logger.info(f"✅ Regla creada: {rule_name}")

        db.commit()
        logger.info("✨ Carga de datos iniciales completada con éxito.")

    except Exception as e:
        logger.error(f"❌ Error durante el seed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_data()
