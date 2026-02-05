# /app/identity/repository_saas.py
"""
Capa de Repositorio para las entidades del modelo de negocio SaaS.
"""
from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from app.identity.models.saas.plan import Plan
from app.identity.models.saas.tenant import Tenant
from app.identity.models.saas.subscription import Subscription
from app.identity.schemas_saas import PlanCreate, PlanUpdate, TenantUpdate, SubscriptionUpdate

class SaasRepository:
    """
    Realiza operaciones CRUD en la base de datos para las entidades SaaS
    como Planes, Tenants y Suscripciones.
    """

    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para Plan ---

    def create_plan(self, plan_in: PlanCreate) -> Plan:
        db_plan = Plan(**plan_in.model_dump())
        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
        return db_plan

    def get_plan_by_id(self, plan_id: uuid.UUID) -> Optional[Plan]:
        return self.db.query(Plan).filter(Plan.id == plan_id).first()

    def get_plan_by_code(self, code: str) -> Optional[Plan]:
        return self.db.query(Plan).filter(Plan.code == code).first()

    def list_plans(self, skip: int = 0, limit: int = 100) -> List[Plan]:
        return self.db.query(Plan).offset(skip).limit(limit).all()

    def update_plan(self, db_plan: Plan, plan_in: PlanUpdate) -> Plan:
        update_data = plan_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_plan, field, value)
        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
        return db_plan

    # --- Métodos para Tenant ---

    def create_tenant(self, name: str, slug: str, partner_id: Optional[uuid.UUID]) -> Tenant:
        db_tenant = Tenant(name=name, slug=slug, partner_id=partner_id)
        self.db.add(db_tenant)
        return db_tenant

    def get_tenant_by_slug(self, slug: str) -> Optional[Tenant]:
        return self.db.query(Tenant).filter(Tenant.slug == slug).first()

    def get_tenant_by_id(self, tenant_id: uuid.UUID) -> Optional[Tenant]:
        return self.db.query(Tenant).options(joinedload(Tenant.subscription).joinedload(Subscription.plan)).filter(Tenant.id == tenant_id).first()

    # --- Métodos para Subscription ---

    def create_subscription(self, tenant_id: uuid.UUID, plan_id: uuid.UUID, start_date: datetime, end_date: datetime) -> Subscription:
        db_subscription = Subscription(
            tenant_id=tenant_id,
            plan_id=plan_id,
            current_period_start=start_date,
            current_period_end=end_date
        )
        self.db.add(db_subscription)
        return db_subscription

    def get_subscription_by_tenant_id(self, tenant_id: uuid.UUID) -> Optional[Subscription]:
        return self.db.query(Subscription).filter(Subscription.tenant_id == tenant_id).first()

    def update_subscription(self, db_subscription: Subscription, sub_in: SubscriptionUpdate) -> Subscription:
        update_data = sub_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_subscription, field, value)
        self.db.add(db_subscription)
        self.db.commit()
        self.db.refresh(db_subscription)
        return db_subscription
