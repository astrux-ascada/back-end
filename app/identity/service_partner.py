# /app/identity/service_partner.py
"""
Servicio para la gestión del Portal de Partners.
"""
import uuid
from typing import List
from sqlalchemy.orm import Session, joinedload

from app.identity.models.saas import Tenant, Subscription, Plan
from app.identity.schemas_saas import PartnerTenantRead

class PartnerService:
    def __init__(self, db: Session):
        self.db = db

    def list_tenants_by_partner(self, partner_id: uuid.UUID) -> List[PartnerTenantRead]:
        """
        Lista todos los tenants gestionados por un partner específico.
        """
        tenants = self.db.query(Tenant).options(
            joinedload(Tenant.subscription).joinedload(Subscription.plan)
        ).filter(Tenant.partner_id == partner_id).all()

        result = []
        for tenant in tenants:
            if tenant.subscription and tenant.subscription.plan:
                result.append(PartnerTenantRead(
                    id=tenant.id,
                    name=tenant.name,
                    slug=tenant.slug,
                    subscription_status=tenant.subscription.status.value if tenant.subscription.status else "N/A",
                    plan_name=tenant.subscription.plan.name
                ))
        
        return result
