import sys
import os
import logging
import uuid
from datetime import datetime, timedelta, timezone

# Agregar el directorio raíz al path para poder importar 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.identity.models.saas.partner import Partner
from app.identity.models.saas.plan import Plan
from app.identity.models.saas.tenant import Tenant, TenantStatus
from app.identity.models.saas.subscription import Subscription, SubscriptionStatus

# Configuración de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_saas_data(db: Session):
    logger.info("🌱 Iniciando Seeding de Datos SaaS...")

    # 1. Crear Partner Global (Astruxa HQ)
    partner = db.query(Partner).filter(Partner.code == "ASTRUXA_HQ").first()
    if not partner:
        partner = Partner(
            code="ASTRUXA_HQ",
            name="Astruxa Global HQ",
            region="GLOBAL",
            currency="USD",
            commission_rate=0.0,
            config={"support_email": "support@astruxa.com"}
        )
        db.add(partner)
        db.commit()
        db.refresh(partner)
        logger.info(f"✅ Partner Global creado: {partner.name}")
    else:
        logger.info(f"ℹ️ Partner Global ya existe: {partner.name}")

    # 2. Crear Planes
    plans_data = [
        {
            "code": "STARTER_V1",
            "name": "Starter Plan",
            "price_monthly": 0.0,
            "limits": {"max_users": 5, "max_assets": 20, "storage_gb": 5},
            "features": {"module_procurement": False, "isolation": "SHARED", "support": "COMMUNITY"}
        },
        {
            "code": "PRO_V1",
            "name": "Professional Plan",
            "price_monthly": 299.0,
            "limits": {"max_users": 50, "max_assets": 500, "storage_gb": 100},
            "features": {"module_procurement": True, "isolation": "SHARED", "support": "EMAIL"}
        },
        {
            "code": "ENTERPRISE_V1",
            "name": "Enterprise Plan",
            "price_monthly": 999.0,
            "limits": {"max_users": 9999, "max_assets": 9999, "storage_gb": 1000},
            "features": {"module_procurement": True, "isolation": "DEDICATED", "support": "24/7"}
        }
    ]

    created_plans = {}
    for p_data in plans_data:
        plan = db.query(Plan).filter(Plan.code == p_data["code"]).first()
        if not plan:
            plan = Plan(**p_data)
            db.add(plan)
            db.commit()
            db.refresh(plan)
            logger.info(f"✅ Plan creado: {plan.name}")
        else:
            logger.info(f"ℹ️ Plan ya existe: {plan.name}")
        created_plans[p_data["code"]] = plan

    # 3. Crear Tenant Demo
    tenant_slug = "demo-plant-01"
    tenant = db.query(Tenant).filter(Tenant.slug == tenant_slug).first()
    
    if not tenant:
        tenant = Tenant(
            partner_id=partner.id,
            name="Planta de Demostración Astruxa",
            slug=tenant_slug,
            status=TenantStatus.ACTIVE,
            db_connection_string=None, # Shared DB
            timezone="America/Mexico_City",
            locale="es-MX",
            config={"theme": "dark"}
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        logger.info(f"✅ Tenant Demo creado: {tenant.name}")

        # 4. Crear Suscripción para el Tenant Demo
        subscription = Subscription(
            tenant_id=tenant.id,
            plan_id=created_plans["PRO_V1"].id,
            status=SubscriptionStatus.ACTIVE,
            current_period_start=datetime.now(timezone.utc),
            current_period_end=datetime.now(timezone.utc) + timedelta(days=365),
            payment_method_id="manual_entry"
        )
        db.add(subscription)
        db.commit()
        logger.info(f"✅ Suscripción PRO activada para: {tenant.name}")
    else:
        logger.info(f"ℹ️ Tenant Demo ya existe: {tenant.name}")

    logger.info("🏁 Seeding SaaS completado exitosamente.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_saas_data(db)
    finally:
        db.close()
