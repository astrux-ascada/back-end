# /app/db/seeding/_seed_identity.py
"""
Seeder para usuarios y roles del sistema (Super Admin, Platform Admin) y del tenant de demostración.
"""
import logging
from sqlalchemy.orm import Session

from app.identity.models import User, Role
from app.core.security import hash_password
from app.core import permissions as p

logger = logging.getLogger(__name__)

async def seed_identity(db: Session, context: dict):
    logger.info("--- [2/9] Poblando Identidad (Usuarios y Roles) ---")
    
    # --- 1. Roles Globales y de Plataforma ---
    roles = ["GLOBAL_SUPER_ADMIN", "PLATFORM_ADMIN"]
    db_roles = {}
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name, description=f"Rol predeterminado {role_name}")
            db.add(role)
            db.commit()
            logger.info(f"✅ Rol creado: {role_name}")
        db_roles[role_name] = role
    
    # --- 2. Usuarios Globales y de Plataforma ---
    
    # 2.1 Super Admin
    super_email = "admin@astruxa.com"
    if not db.query(User).filter(User.email == super_email).first():
        super_user = User(
            email=super_email,
            name="Super Admin",
            hashed_password=hash_password("admin123"),
            is_active=True,
            is_superuser=True
        )
        super_user.roles.append(db_roles["GLOBAL_SUPER_ADMIN"])
        db.add(super_user)
        db.commit()
        logger.info(f"✅ Superusuario creado: {super_email}")

    # 2.2 Platform Admin
    platform_email = "platform@astruxa.com"
    if not db.query(User).filter(User.email == platform_email).first():
        platform_user = User(
            email=platform_email,
            name="Platform Manager",
            hashed_password=hash_password("platform123"),
            is_active=True
        )
        platform_user.roles.append(db_roles["PLATFORM_ADMIN"])
        db.add(platform_user)
        db.commit()
        logger.info(f"✅ Platform Admin creado: {platform_email}")

    # --- 3. Identidad del Tenant Demo ---
    
    demo_tenant = context.get("demo_tenant")
    if demo_tenant:
        permissions_map = context.get("permissions_map", {})

        # 3.1 Rol de Operador
        operator_role = db.query(Role).filter(Role.name == "OPERATOR", Role.tenant_id == demo_tenant.id).first()
        if not operator_role:
            operator_role = Role(name="OPERATOR", description="Operador de planta", tenant_id=demo_tenant.id)
            # Asignar permisos básicos
            operator_perms = [
                p.ASSET_READ, p.WORK_ORDER_READ, p.WORK_ORDER_UPDATE, 
                p.ALARM_READ, p.ALARM_ACKNOWLEDGE
            ]
            operator_role.permissions = [permissions_map[perm] for perm in operator_perms if perm in permissions_map]
            db.add(operator_role)
            db.commit()

        # 3.2 Usuario Operador
        operator_user = db.query(User).filter(User.email == "operator@demo.com").first()
        if not operator_user:
            operator_user = User(
                email="operator@demo.com",
                hashed_password=hash_password("demo_password"),
                name="Juan Operador",
                is_active=True,
                tenant_id=demo_tenant.id
            )
            operator_user.roles.append(operator_role)
            db.add(operator_user)
            db.commit()
        
        # Guardar en el contexto para los siguientes seeders
        context["operator_user"] = operator_user
    
    # Guardar roles globales en el contexto por si se necesitan
    context["global_roles"] = db_roles
