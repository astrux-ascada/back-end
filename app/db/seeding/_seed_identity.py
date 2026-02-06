# /app/db/seeding/_seed_identity.py
"""
Seeder para usuarios y roles adicionales del tenant de demostración.
"""
import logging
from sqlalchemy.orm import Session

from app.identity.models import User, Role
from app.core.security import hash_password
from app.core import permissions as p

logger = logging.getLogger(__name__)

async def seed_identity(db: Session, context: dict):
    logger.info("--- [2/9] Poblando Identidad (Usuarios y Roles) ---")
    
    demo_tenant = context["demo_tenant"]
    permissions_map = context["permissions_map"]

    # 1. Rol de Operador
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

    # 2. Usuario Operador
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
