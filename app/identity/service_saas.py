# /app/identity/service_saas.py
"""
Capa de Servicio para la gestión del modelo de negocio SaaS.
"""
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.identity.models.saas import Plan, Tenant, Subscription
from app.identity.schemas_saas import PlanCreate, PlanUpdate, TenantCreate, TenantUpdate, SubscriptionUpdate, PublicRegistrationRequest
from app.identity.auth_service import AuthService
from app.core.exceptions import NotFoundException, ConflictException, PermissionDeniedException
from app.core.error_messages import ErrorMessages
from slugify import slugify

class SaasService:
    """Servicio de negocio para la gestión de Planes, Tenants y Suscripciones."""

    def __init__(self, db: Session, auth_service: AuthService):
        self.db = db
        self.auth_service = auth_service

    # --- Métodos para Planes ---
    def create_plan(self, plan_in: PlanCreate) -> Plan:
        db_plan = Plan(**plan_in.model_dump())
        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
        return db_plan

    def list_plans(self, skip: int = 0, limit: int = 100) -> List[Plan]:
        return self.db.query(Plan).offset(skip).limit(limit).all()

    def get_plan(self, plan_id: uuid.UUID) -> Plan:
        plan = self.db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise NotFoundException(ErrorMessages.PLAN_NOT_FOUND)
        return plan

    def update_plan(self, plan_id: uuid.UUID, plan_in: PlanUpdate) -> Plan:
        db_plan = self.get_plan(plan_id)
        update_data = plan_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_plan, field, value)
        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
        return db_plan

    # --- Métodos para Tenants y Suscripciones ---
    def get_tenant(self, tenant_id: uuid.UUID) -> Tenant:
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id, Tenant.deleted_at == None).first()
        if not tenant:
            raise NotFoundException(ErrorMessages.TENANT_NOT_FOUND)
        return tenant

    def list_tenants(self, skip: int = 0, limit: int = 100) -> List[Tenant]:
        return self.db.query(Tenant).filter(Tenant.deleted_at == None).offset(skip).limit(limit).all()

    def update_tenant(self, tenant_id: uuid.UUID, tenant_in: TenantUpdate) -> Tenant:
        db_tenant = self.get_tenant(tenant_id)
        update_data = tenant_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tenant, field, value)
        self.db.add(db_tenant)
        self.db.commit()
        self.db.refresh(db_tenant)
        return db_tenant

    def delete_tenant(self, tenant_id: uuid.UUID, confirmation_key: str) -> Tenant:
        db_tenant = self.get_tenant(tenant_id)
        
        # Clave de confirmación simple: el slug del tenant
        if confirmation_key != db_tenant.slug:
            raise PermissionDeniedException(ErrorMessages.TENANT_DELETION_CONFIRMATION_INVALID)
            
        # Borrado lógico
        db_tenant.deleted_at = datetime.now(timezone.utc)
        db_tenant.is_active = False
        self.db.add(db_tenant)
        self.db.commit()
        self.db.refresh(db_tenant)
        
        # Aquí se podría disparar un evento para un borrado físico asíncrono en el futuro
        # self.event_broker.publish("tenant:deleted", {"tenant_id": tenant_id})
        
        return db_tenant

    def update_subscription(self, tenant_id: uuid.UUID, sub_in: SubscriptionUpdate) -> Subscription:
        subscription = self.db.query(Subscription).filter(Subscription.tenant_id == tenant_id).first()
        if not subscription:
            raise NotFoundException("Suscripción no encontrada.")
        
        self.get_plan(sub_in.plan_id)
        
        subscription.plan_id = sub_in.plan_id
        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    def public_registration(self, registration_in: PublicRegistrationRequest) -> Tenant:
        if self.auth_service.get_user_by_email(registration_in.admin_email):
            raise ConflictException(ErrorMessages.AUTH_EMAIL_ALREADY_EXISTS)

        plan = self.get_plan(registration_in.plan_id)

        tenant_slug = slugify(registration_in.company_name)
        if self.db.query(Tenant).filter(Tenant.slug == tenant_slug).first():
            tenant_slug = f"{tenant_slug}-{uuid.uuid4().hex[:6]}"
        
        db_tenant = Tenant(name=registration_in.company_name, slug=tenant_slug)
        self.db.add(db_tenant)
        self.db.flush()

        admin_role = self.auth_service.create_tenant_admin_role(db_tenant.id)

        self.auth_service.create_user(
            email=registration_in.admin_email,
            name=registration_in.admin_name,
            password=registration_in.admin_password,
            tenant_id=db_tenant.id,
            roles=[admin_role]
        )

        period_end = datetime.utcnow() + timedelta(days=30) if plan.price_monthly == 0 else None
        
        subscription = Subscription(
            tenant_id=db_tenant.id,
            plan_id=plan.id,
            current_period_start=datetime.utcnow(),
            current_period_end=period_end,
            is_active=(plan.price_monthly == 0)
        )
        self.db.add(subscription)

        self.db.commit()
        self.db.refresh(db_tenant)
        return db_tenant
