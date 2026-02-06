# /app/identity/service_saas.py
"""
Capa de Servicio para la gestión del modelo de negocio SaaS.
"""
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.identity.models.saas import Plan, Tenant, Subscription
from app.identity.schemas_saas import PlanCreate, PlanUpdate, TenantCreate, SubscriptionUpdate, PublicRegistrationRequest
from app.identity.auth_service import AuthService
from app.core.exceptions import NotFoundException, ConflictException
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
            raise NotFoundException("Plan no encontrado.")
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
    def create_tenant_and_admin(self, tenant_in: TenantCreate) -> Tenant:
        # Lógica existente para creación por un Super Admin
        # (Se puede refactorizar para reutilizarla en public_registration)
        pass

    def get_tenant(self, tenant_id: uuid.UUID) -> Tenant:
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise NotFoundException("Tenant no encontrado.")
        return tenant

    def update_subscription(self, tenant_id: uuid.UUID, sub_in: SubscriptionUpdate) -> Subscription:
        subscription = self.db.query(Subscription).filter(Subscription.tenant_id == tenant_id).first()
        if not subscription:
            raise NotFoundException("Suscripción no encontrada.")
        
        # Validar que el nuevo plan existe
        self.get_plan(sub_in.plan_id)
        
        subscription.plan_id = sub_in.plan_id
        # Aquí podría haber lógica para prorrateo, etc.
        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    def public_registration(self, registration_in: PublicRegistrationRequest) -> Tenant:
        """
        Orquesta el proceso de registro público de un nuevo tenant.
        """
        # 1. Validar que el email no exista
        if self.auth_service.get_user_by_email(registration_in.admin_email):
            raise ConflictException("El email ya está registrado.")

        # 2. Validar que el plan seleccionado existe
        plan = self.get_plan(registration_in.plan_id)

        # 3. Crear el Tenant
        tenant_slug = slugify(registration_in.company_name)
        if self.db.query(Tenant).filter(Tenant.slug == tenant_slug).first():
            tenant_slug = f"{tenant_slug}-{uuid.uuid4().hex[:6]}" # Añadir aleatoriedad si el slug ya existe
        
        db_tenant = Tenant(name=registration_in.company_name, slug=tenant_slug)
        self.db.add(db_tenant)
        self.db.flush() # Para obtener el ID del tenant

        # 4. Crear el rol de Admin para este Tenant
        admin_role = self.auth_service.create_tenant_admin_role(db_tenant.id)

        # 5. Crear el usuario Administrador
        admin_user = self.auth_service.create_user(
            email=registration_in.admin_email,
            name=registration_in.admin_name,
            password=registration_in.admin_password,
            tenant_id=db_tenant.id,
            roles=[admin_role]
        )

        # 6. Crear la Suscripción
        # Para planes de pago, el periodo podría ser 0 hasta que se confirme el pago.
        # Para planes gratuitos, se activa inmediatamente.
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
