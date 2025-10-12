# /app/db/seeding/_seed_identity.py
"""
Script para sembrar la base de datos con datos iniciales de Identidad (Permisos, Roles, Usuario Admin).
"""
import logging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.identity.models import Permission, Role, User
from app.identity.schemas import UserCreate
from app.identity.repository import UserRepository

logger = logging.getLogger(__name__)

# --- Definición de Permisos Esenciales ---
# Estructura: "entidad:acción"
PERMISSIONS = [
    # Permisos de Activos
    "asset:create", "asset:read", "asset:update", "asset:delete",
    # Permisos de Usuarios
    "user:create", "user:read", "user:update", "user:delete",
    # Permisos de Roles
    "role:create", "role:read", "role:update", "role:delete",
    # Permisos de Sectores
    "sector:create", "sector:read", "sector:update", "sector:delete",
    # Permisos de Mantenimiento
    "maintenance:create", "maintenance:read", "maintenance:update",
    # Permisos de Compras
    "procurement:create", "procurement:read", "procurement:update",
    # Permisos de Telemetría y Alertas
    "telemetry:read", "alarming:read", "alarming:update",
    # Permisos de Auditoría
    "auditing:read"
]

def seed_identity(db: Session) -> None:
    """Crea permisos, roles y un usuario superusuario si no existen."""
    logger.info("Iniciando el sembrado de datos de Identidad...")

    # --- 1. Crear Permisos ---
    all_permissions = []
    for perm_name in PERMISSIONS:
        db_perm = db.query(Permission).filter(Permission.name == perm_name).first()
        if not db_perm:
            db_perm = Permission(name=perm_name, description=f"Permite la acción '{perm_name.split(':')[1]}' en la entidad '{perm_name.split(':')[0]}'.")
            db.add(db_perm)
            logger.info(f"Creando permiso: {perm_name}")
        all_permissions.append(db_perm)
    db.commit()

    # --- 2. Crear Roles Estandarizados ---
    
    # Rol de Super User
    super_user_role = db.query(Role).filter(Role.name == "Super User").first()
    if not super_user_role:
        super_user_role = Role(name="Super User", description="Acceso total a todas las funcionalidades del sistema.")
        super_user_role.permissions = all_permissions
        db.add(super_user_role)
        logger.info("Creando rol estandarizado: Super User")

    # Rol de Admin
    admin_role = db.query(Role).filter(Role.name == "Admin").first()
    if not admin_role:
        # Los Admins tienen todos los permisos excepto la gestión de roles.
        admin_permissions = [p for p in all_permissions if not p.name.startswith("role:")]
        admin_role = Role(name="Admin", description="Acceso administrativo para la gestión de usuarios, activos y otras funcionalidades, pero sin permiso para gestionar roles.")
        admin_role.permissions = admin_permissions
        db.add(admin_role)
        logger.info("Creando rol estandarizado: Admin")

    # Rol de Operador
    operator_role = db.query(Role).filter(Role.name == "Operator").first()
    if not operator_role:
        operator_permissions = [p for p in all_permissions if "read" in p.name]
        operator_role = Role(name="Operator", description="Acceso de solo lectura a la mayoría de las funcionalidades.")
        operator_role.permissions = operator_permissions
        db.add(operator_role)
        logger.info("Creando rol estandarizado: Operator")
    db.commit()

    # --- 3. Crear Usuario Super User ---
    superuser_user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER_EMAIL).first()
    if not superuser_user:
        user_repo = UserRepository(db)
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            name="Super User",
            role_ids=[super_user_role.id]
        )
        superuser_user = user_repo.create(user_in=user_in)
        logger.info(f"Creando usuario Super User: {settings.FIRST_SUPERUSER_EMAIL}")
    else:
        logger.info("El usuario Super User ya existe, no se realizaron cambios.")

    logger.info("Sembrado de datos de Identidad completado.")
