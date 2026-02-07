# /app/identity/api_saas.py
"""
API Router para la gestión del modelo de negocio SaaS (Planes, Tenants, etc.).
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException

from app.dependencies.permissions import require_permission
from app.dependencies.services import get_saas_service, get_usage_service
from app.dependencies.tenant import get_tenant_id
from app.identity.service_saas import SaasService
from app.identity.service_usage import UsageService
from app.identity.schemas_saas import (
    PlanCreate, PlanUpdate, PlanRead, 
    TenantCreate, TenantUpdate, TenantRead, TenantDeletionConfirmation,
    SubscriptionUpdate, SubscriptionRead,
    PublicRegistrationRequest,
    UsageReport
)

router = APIRouter(
    prefix="/saas", 
    tags=["SaaS Management"]
)

# --- Endpoints Públicos (Auto-Suscripción) ---

@router.post("/public/register", response_model=TenantRead, status_code=status.HTTP_201_CREATED)
def public_registration(
    registration_in: PublicRegistrationRequest,
    saas_service: SaasService = Depends(get_saas_service)
):
    try:
        return saas_service.public_registration(registration_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# --- Endpoints para el Portal de Cliente (Autogestión) ---

@router.get("/usage", response_model=UsageReport, dependencies=[Depends(require_permission("tenant:read"))])
def get_tenant_usage(
    usage_service: UsageService = Depends(get_usage_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """Devuelve un reporte del uso de recursos actual del tenant."""
    return usage_service.get_usage_report(tenant_id)

@router.get("/my-tenant", response_model=TenantRead, dependencies=[Depends(require_permission("tenant:read"))])
def get_my_tenant_details(
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    saas_service: SaasService = Depends(get_saas_service)
):
    """Devuelve los detalles completos del tenant del usuario autenticado."""
    return saas_service.get_tenant(tenant_id)

@router.put("/my-tenant", response_model=TenantRead, dependencies=[Depends(require_permission("tenant:update"))])
def update_my_tenant_details(
    tenant_in: TenantUpdate,
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    saas_service: SaasService = Depends(get_saas_service)
):
    """Permite a un admin de tenant actualizar los datos de su propia empresa."""
    return saas_service.update_tenant(tenant_id, tenant_in)


# --- Endpoints para Planes (Gestión de Super Admin) ---

@router.post("/plans", response_model=PlanRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("plan:create"))])
def create_plan(plan_in: PlanCreate, saas_service: SaasService = Depends(get_saas_service)):
    return saas_service.create_plan(plan_in)

@router.get("/plans", response_model=List[PlanRead], dependencies=[Depends(require_permission("plan:read"))])
def list_plans(skip: int = 0, limit: int = 100, saas_service: SaasService = Depends(get_saas_service)):
    return saas_service.list_plans(skip, limit)

@router.get("/plans/{plan_id}", response_model=PlanRead, dependencies=[Depends(require_permission("plan:read"))])
def get_plan(plan_id: uuid.UUID, saas_service: SaasService = Depends(get_saas_service)):
    return saas_service.get_plan(plan_id)

@router.put("/plans/{plan_id}", response_model=PlanRead, dependencies=[Depends(require_permission("plan:update"))])
def update_plan(plan_id: uuid.UUID, plan_in: PlanUpdate, saas_service: SaasService = Depends(get_saas_service)):
    return saas_service.update_plan(plan_id, plan_in)


# --- Endpoints para Tenants (Gestión de Super Admin) ---

@router.get("/tenants", response_model=List[TenantRead], dependencies=[Depends(require_permission("tenant:read"))])
def list_tenants(
    skip: int = 0,
    limit: int = 100,
    saas_service: SaasService = Depends(get_saas_service)
):
    """(Super Admin) Lista todos los tenants activos en la plataforma."""
    return saas_service.list_tenants(skip, limit)

@router.post("/tenants", response_model=TenantRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("tenant:create"))])
def create_tenant(tenant_in: TenantCreate, saas_service: SaasService = Depends(get_saas_service)):
    # Este endpoint es para que un Super Admin cree un tenant manualmente.
    # La lógica podría ser diferente a la del registro público.
    # Por ahora, asumimos que es similar.
    pass

@router.get("/tenants/{tenant_id}", response_model=TenantRead, dependencies=[Depends(require_permission("tenant:read"))])
def get_tenant(tenant_id: uuid.UUID, saas_service: SaasService = Depends(get_saas_service)):
    return saas_service.get_tenant(tenant_id)

@router.put("/tenants/{tenant_id}", response_model=TenantRead, dependencies=[Depends(require_permission("tenant:update"))])
def update_tenant(
    tenant_id: uuid.UUID,
    tenant_in: TenantUpdate,
    saas_service: SaasService = Depends(get_saas_service)
):
    """(Super Admin) Actualiza los datos de cualquier tenant."""
    return saas_service.update_tenant(tenant_id, tenant_in)

@router.delete("/tenants/{tenant_id}", response_model=TenantRead, dependencies=[Depends(require_permission("tenant:delete"))])
def delete_tenant(
    tenant_id: uuid.UUID,
    confirmation: TenantDeletionConfirmation,
    saas_service: SaasService = Depends(get_saas_service)
):
    """(Super Admin) Realiza un borrado lógico de un tenant."""
    return saas_service.delete_tenant(tenant_id, confirmation.confirmation_key)


# --- Endpoints para Suscripciones (Gestión de Super Admin) ---

@router.put("/tenants/{tenant_id}/subscription", response_model=SubscriptionRead, dependencies=[Depends(require_permission("subscription:update"))])
def update_subscription(
    tenant_id: uuid.UUID,
    sub_in: SubscriptionUpdate,
    saas_service: SaasService = Depends(get_saas_service)
):
    try:
        return saas_service.update_subscription(tenant_id, sub_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
