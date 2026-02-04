# /app/identity/service_saas.py
"""
Capa de Servicio para la gestión del modelo de negocio SaaS.
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from slugify import slugify

from app.core.exceptions import NotFoundException, ConflictException
from app.identity.models.saas.plan import Plan
from app.identity.models.saas.tenant import Tenant
from app.identity.models.saas.subscription import Subscription
from app.identity.repository_saas import SaasRepository
from app.identity.schemas_saas import PlanCreate, PlanUpdate, TenantCreate, SubscriptionUpdate
from app.identity.auth_service import AuthService
from app.identity.schemas import UserCreate

class SaasService:
    """
    Servicio de negocio para la gestión de Planes, Tenants y Suscripciones.
    """

    def __init__(self, db: Session, auth_service: AuthService):
        self.db = db
        self.auth_service = auth_service
        self.saas_repo = SaasRepository(db)

    # --- Métodos para Plan ---
    def create_plan(self, plan_in: PlanCreate) -> Plan:
        existing_plan = self.saas_repo.get_plan_by_code(plan_in.code)
        if existing_plan:
            raise ConflictException(f"Ya existe un plan con el código '{plan_in.code}'.")
        return self.saas_repo.create_plan(plan_in)

    def get_plan(self, plan_id: uuid.UUID) -> Plan:
        db_plan = self.saas_repo.get_plan_by_id(plan_id)
        if not db_plan:
            raise NotFoundException("Plan no encontrado.")
        return db_plan

    def list_plans(self, skip: int = 0, limit: int = 100) -> List[Plan]:
        return self.saas_repo.list_plans(skip, limit)

    def update_plan(self, plan_id: uuid.UUID, plan_in: PlanUpdate) -> Plan:
        db_plan = self.get_plan(plan_id)
        return self.saas_repo.update_plan(db_plan, plan_in)

    # --- Métodos para Tenant ---
    def create_tenant_and_admin(self, tenant_in: TenantCreate) -> Tenant:
        plan = self.saas_repo.get_plan_by_id(tenant_in.plan_id)
        if not plan:
            raise NotFoundException(f"El plan con ID '{tenant_in.plan_id}' no existe.")
        tenant_slug = slugify(tenant_in.name)
        if self.saas_repo.get_tenant_by_slug(tenant_slug):
            raise ConflictException(f"Ya existe un tenant con el nombre '{tenant_in.name}'.")
        try:
            db_tenant = self.saas_repo.create_tenant(name=tenant_in.name, slug=tenant_slug, partner_id=tenant_in.partner_id)
            self.db.flush()
            admin_user_data = UserCreate(email=tenant_in.admin_email, password=tenant_in.admin_password)
            self.auth_service.register_user(admin_user_data, tenant_id=db_tenant.id)
            start_date = datetime.utcnow()
            end_date = start_date + timedelta(days=365)
            self.saas_repo.create_subscription(tenant_id=db_tenant.id, plan_id=plan.id, start_date=start_date, end_date=end_date)
            self.db.commit()
            self.db.refresh(db_tenant)
            return db_tenant
        except Exception as e:
            self.db.rollback()
            raise e
            
    def get_tenant(self, tenant_id: uuid.UUID) -> Tenant:
        db_tenant = self.saas_repo.get_tenant_by_id(tenant_id)
        if not db_tenant:
            raise NotFoundException("Tenant no encontrado.")
        return db_tenant

    # --- Métodos para Subscription ---
    def update_subscription(self, tenant_id: uuid.UUID, sub_in: SubscriptionUpdate) -> Subscription:
        """
        Actualiza la suscripción de un tenant.
        Permite cambiar el plan, el estado o la fecha de fin.
        """
        db_subscription = self.saas_repo.get_subscription_by_tenant_id(tenant_id)
        if not db_subscription:
            raise NotFoundException("Suscripción no encontrada para este tenant.")

        # Si se cambia el plan, validar que el nuevo plan exista
        if sub_in.plan_id:
            new_plan = self.saas_repo.get_plan_by_id(sub_in.plan_id)
            if not new_plan:
                raise NotFoundException(f"El nuevo plan con ID '{sub_in.plan_id}' no existe.")

        return self.saas_repo.update_subscription(db_subscription, sub_in)
