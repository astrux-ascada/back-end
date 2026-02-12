import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy import text

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Entorno y Configuración ---
load_dotenv(os.path.join(os.getcwd(), ".env"))

if os.environ.get("POSTGRES_HOST") == "backend_db":
    logger.info("🔄 Configurando entorno local (localhost:5433)...")
    os.environ["POSTGRES_HOST"] = "localhost"
    os.environ["POSTGRES_PORT"] = "5433"
if os.environ.get("REDIS_HOST") == "redis":
    os.environ["REDIS_HOST"] = "localhost"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.core.database import SessionLocal
from app.identity.models import User, Role, Permission
from app.notifications.models import NotificationChannel, NotificationTemplate, NotificationRule, NotificationChannelType, NotificationRecipientType, NotificationLevel
from app.core.security import hash_password
from app.core import permissions as p

# --- Lista completa de permisos ---
ALL_PERMISSIONS = [
    # SaaS
    p.PLAN_READ, p.PLAN_CREATE, p.PLAN_UPDATE,
    p.TENANT_READ, p.TENANT_READ_ALL, p.TENANT_CREATE, p.TENANT_UPDATE, p.TENANT_ASSIGN_MANAGER,
    p.TENANT_DELETE_REQUEST, p.TENANT_DELETE_APPROVE, p.TENANT_DELETE_FORCE,
    p.SUBSCRIPTION_READ, p.SUBSCRIPTION_UPDATE,
    # Marketing
    p.CAMPAIGN_READ, p.CAMPAIGN_CREATE, p.CAMPAIGN_UPDATE, p.CAMPAIGN_DELETE,
    p.COUPON_READ, p.COUPON_CREATE, p.COUPON_UPDATE, p.COUPON_DELETE, p.COUPON_APPLY,
    p.REFERRAL_READ,
    # Identity
    p.USER_READ, p.USER_CREATE, p.USER_UPDATE, p.USER_DELETE,
    p.USER_READ_ALL, p.USER_CREATE_ANY, p.USER_UPDATE_ANY, p.USER_DELETE_ANY,
    p.USER_CREATE_ADMIN,
    p.ROLE_READ, p.ROLE_CREATE, p.ROLE_UPDATE, p.ROLE_DELETE,
    p.PERMISSION_READ, p.SESSION_DELETE,
    # ... (se pueden añadir el resto de permisos operativos si se desea)
]

PLATFORM_ADMIN_PERMISSIONS = p.DEFAULT_PLATFORM_ADMIN_PERMISSIONS

def create_initial_data():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        logger.info("✅ Conexión a BD establecida.")
    except Exception as e:
        logger.error(f"❌ Error conectando a la BD: {e}")
        return

    try:
        logger.info("🌱 Iniciando carga de datos...")

        # 1. Permisos
        logger.info("--- [1/4] Gestionando Permisos ---")
        permissions_map = {perm.name: perm for perm in db.query(Permission).all()}
        for perm_name in ALL_PERMISSIONS:
            if perm_name not in permissions_map:
                db_perm = Permission(name=perm_name, description=f"Permite: {perm_name}")
                db.add(db_perm)
                permissions_map[perm_name] = db_perm
        db.flush()

        # 2. Roles
        logger.info("--- [2/4] Gestionando Roles ---")
        super_role = db.query(Role).filter(Role.name == "GLOBAL_SUPER_ADMIN").first()
        if not super_role:
            super_role = Role(name="GLOBAL_SUPER_ADMIN", description="Acceso total.", tenant_id=None)
            db.add(super_role)
        super_role.permissions = list(permissions_map.values())
        logger.info("   > Permisos actualizados para GLOBAL_SUPER_ADMIN")

        platform_role = db.query(Role).filter(Role.name == "PLATFORM_ADMIN").first()
        if not platform_role:
            platform_role = Role(name="PLATFORM_ADMIN", description="Gestión operativa.", tenant_id=None)
            db.add(platform_role)
        platform_role.permissions = [permissions_map[p_name] for p_name in PLATFORM_ADMIN_PERMISSIONS if p_name in permissions_map]
        logger.info("   > Permisos actualizados para PLATFORM_ADMIN")

        db.flush()

        # 3. Usuarios
        logger.info("--- [3/4] Gestionando Usuarios ---")
        super_user = db.query(User).filter(User.email == "admin@astruxa.com").first()
        if not super_user:
            super_user = User(email="admin@astruxa.com", name="Super Admin", hashed_password=hash_password("admin123"), is_active=True)
            super_user.roles.append(super_role)
            db.add(super_user)
        
        # 4. Notificaciones (simplificado)
        logger.info("--- [4/4] Configurando Notificaciones ---")
        if not db.query(NotificationChannel).filter(NotificationChannel.type == NotificationChannelType.IN_APP).first():
            db.add(NotificationChannel(name="In-App Notifications", type=NotificationChannelType.IN_APP, is_active=True))

        db.commit()
        logger.info("✨ Carga de datos iniciales completada con éxito.")

    except Exception as e:
        logger.error(f"❌ Error durante el seed: {e}")
        db.rollback()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    create_initial_data()
