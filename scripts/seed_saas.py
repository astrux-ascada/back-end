# /scripts/seed_saas.py
"""
Script para poblar la base de datos con datos maestros para el modelo SaaS.
"""
import sys
import os
import asyncio
import logging
from datetime import datetime, timedelta

# --- Añadir el directorio raíz del proyecto al PYTHONPATH ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------------------------------------------------

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.config import settings
from app.core import permissions as p
from app.identity.models.saas.plan import Plan
from app.identity.models.saas.partner import Partner
from app.identity.models.saas.tenant import Tenant
from app.identity.models.saas.subscription import Subscription, SubscriptionStatus # Corregir importación
from app.identity.models import User, Role, Permission
from app.core.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- DATOS MAESTROS ---

ALL_PERMISSIONS = [
    p.PLAN_READ, p.PLAN_CREATE, p.PLAN_UPDATE,
    p.TENANT_READ, p.TENANT_CREATE, p.TENANT_UPDATE,
    p.SUBSCRIPTION_READ, p.SUBSCRIPTION_UPDATE,
    p.ASSET_READ, p.ASSET_CREATE, p.ASSET_UPDATE, p.ASSET_UPDATE_STATUS, p.ASSET_DELETE,
    p.WORK_ORDER_READ, p.WORK_ORDER_CREATE, p.WORK_ORDER_UPDATE, p.WORK_ORDER_CANCEL, p.WORK_ORDER_ASSIGN_PROVIDER, p.WORK_ORDER_EVALUATE,
    p.PROVIDER_READ, p.PROVIDER_CREATE, p.PROVIDER_UPDATE, p.PROVIDER_DELETE,
    p.SPARE_PART_READ, p.SPARE_PART_CREATE, p.SPARE_PART_UPDATE, p.SPARE_PART_DELETE,
    p.RFQ_CREATE, p.RFQ_READ, p.QUOTE_SUBMIT, p.QUOTE_EVALUATE, p.PO_CREATE, p.PO_READ, p.PO_RECEIVE,
    p.ALARM_RULE_READ, p.ALARM_RULE_CREATE, p.ALARM_RULE_UPDATE, p.ALARM_RULE_DELETE,
    p.ALARM_READ, p.ALARM_ACKNOWLEDGE,
    p.SECTOR_READ, p.SECTOR_CREATE, p.SECTOR_UPDATE, p.SECTOR_DELETE,
    p.CONFIG_PARAM_READ, p.CONFIG_PARAM_CREATE, p.CONFIG_PARAM_UPDATE, p.CONFIG_PARAM_DELETE,
    p.DATA_SOURCE_READ, p.DATA_SOURCE_CREATE, p.DATA_SOURCE_UPDATE, p.DATA_SOURCE_DELETE,
    p.AUDIT_LOG_READ, p.APPROVAL_READ, p.APPROVAL_DECIDE,
    p.USER_READ, p.USER_CREATE, p.USER_UPDATE, p.USER_DELETE,
    p.ROLE_READ, p.ROLE_CREATE, p.ROLE_UPDATE, p.ROLE_DELETE,
    p.PERMISSION_READ, p.SESSION_DELETE
]

TENANT_ADMIN_PERMISSIONS = [
    p.ASSET_READ, p.ASSET_CREATE, p.ASSET_UPDATE, p.ASSET_DELETE,
    p.WORK_ORDER_READ, p.WORK_ORDER_CREATE, p.WORK_ORDER_UPDATE, p.WORK_ORDER_CANCEL, p.WORK_ORDER_ASSIGN_PROVIDER, p.WORK_ORDER_EVALUATE,
    p.PROVIDER_READ, p.PROVIDER_CREATE, p.PROVIDER_UPDATE, p.PROVIDER_DELETE,
    p.SPARE_PART_READ, p.SPARE_PART_CREATE, p.SPARE_PART_UPDATE, p.SPARE_PART_DELETE,
    p.RFQ_CREATE, p.RFQ_READ, p.QUOTE_EVALUATE, p.PO_CREATE, p.PO_READ, p.PO_RECEIVE,
    p.ALARM_RULE_READ, p.ALARM_RULE_CREATE, p.ALARM_RULE_UPDATE, p.ALARM_RULE_DELETE,
    p.ALARM_READ, p.ALARM_ACKNOWLEDGE,
    p.SECTOR_READ, p.SECTOR_CREATE, p.SECTOR_UPDATE, p.SECTOR_DELETE,
    p.AUDIT_LOG_READ, p.APPROVAL_READ, p.APPROVAL_DECIDE,
    p.USER_READ, p.USER_CREATE, p.USER_UPDATE, p.USER_DELETE,
    p.ROLE_READ, p.ROLE_CREATE, p.ROLE_UPDATE, p.ROLE_DELETE,
]

async def seed_data(db: Session):
    logger.info("Iniciando el proceso de seeding para el entorno SaaS...")

    # 1. Crear todos los permisos
    permissions_map = {}
    for perm_name in ALL_PERMISSIONS:
        db_perm = db.query(Permission).filter(Permission.name == perm_name).first()
        if not db_perm:
            db_perm = Permission(name=perm_name, description=f"Permite la acción: {perm_name}")
            db.add(db_perm)
        permissions_map[perm_name] = db_perm
    db.commit()
    logger.info(f"Se han creado/verificado {len(permissions_map)} permisos.")

    # 2. Crear Rol de Super Admin Global
    super_admin_role = db.query(Role).filter(Role.name == "GLOBAL_SUPER_ADMIN").first()
    if not super_admin_role:
        super_admin_role = Role(name="GLOBAL_SUPER_ADMIN", description="Acceso total a la plataforma.", tenant_id=None)
        super_admin_role.permissions = list(permissions_map.values())
        db.add(super_admin_role)
    db.commit()
    logger.info("Rol GLOBAL_SUPER_ADMIN creado y asignado todos los permisos.")

    # 3. Crear el usuario Super Admin Global
    super_admin_user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER_EMAIL).first()
    if not super_admin_user:
        super_admin_user = User(
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=hash_password(settings.FIRST_SUPERUSER_PASSWORD),
            name="Global Super Admin",
            is_active=True,
            tenant_id=None
        )
        super_admin_user.roles.append(super_admin_role)
        db.add(super_admin_user)
    db.commit()
    logger.info("Usuario Super Admin Global creado.")

    # 4. Crear el Partner Global por defecto
    global_partner = db.query(Partner).filter(Partner.name == "Astruxa Global").first()
    if not global_partner:
        global_partner = Partner(name="Astruxa Global", code="ASTRUXA_GLOBAL")
        db.add(global_partner)
    db.commit()
    logger.info("Partner Global creado.")

    # 5. Crear Planes de ejemplo
    if not db.query(Plan).first():
        plans_data = [
            {"code": "FREE", "name": "Free Tier", "price_monthly": 0, "price_yearly": 0, "limits": {"max_users": 1, "max_assets": 5}},
            {"code": "PRO", "name": "Professional", "price_monthly": 99, "price_yearly": 999, "limits": {"max_users": 10, "max_assets": 100}, "features": {"module_procurement": True}},
            {"code": "ENTERPRISE", "name": "Enterprise", "price_monthly": 499, "price_yearly": 4999, "limits": {"max_users": -1, "max_assets": -1}, "features": {"module_procurement": True, "api_access": True}},
        ]
        for plan_data in plans_data:
            db.add(Plan(**plan_data))
        db.commit()
        logger.info("Planes de ejemplo creados.")

    # 6. Crear un Tenant de Demostración
    demo_tenant = db.query(Tenant).filter(Tenant.slug == "demo-tenant").first()
    if not demo_tenant:
        demo_tenant = Tenant(name="Demo Tenant", slug="demo-tenant", partner_id=global_partner.id)
        db.add(demo_tenant)
        db.commit()
        
        # Crear rol de Admin para este tenant
        tenant_admin_role = Role(name="TENANT_ADMIN", description="Administrador del Tenant", tenant_id=demo_tenant.id)
        tenant_admin_role.permissions = [permissions_map[p_name] for p_name in TENANT_ADMIN_PERMISSIONS]
        db.add(tenant_admin_role)
        
        # Crear usuario admin para el tenant
        demo_admin_user = User(
            email="admin@demo.com",
            hashed_password=hash_password("demo_password"),
            name="Demo Admin",
            is_active=True,
            tenant_id=demo_tenant.id
        )
        demo_admin_user.roles.append(tenant_admin_role)
        db.add(demo_admin_user)
        
        # Crear suscripción para el tenant
        pro_plan = db.query(Plan).filter(Plan.code == "PRO").first()
        subscription = Subscription(
            tenant_id=demo_tenant.id,
            plan_id=pro_plan.id,
            status=SubscriptionStatus.ACTIVE,
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=365)
        )
        db.add(subscription)
        
        db.commit()
        logger.info("Tenant de Demostración, con su admin y suscripción, creado.")

    logger.info("Proceso de seeding finalizado con éxito.")

async def main():
    db = SessionLocal()
    try:
        await seed_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
