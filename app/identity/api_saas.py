# /app/identity/api_saas.py
"""
API Router para la gestión del modelo de negocio SaaS (Planes, Tenants, etc.).
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException

from app.dependencies.permissions import require_permission # Importar el nuevo sistema
from app.dependencies.services import get_saas_service
from app.identity.service_saas import SaasService
from app.identity.schemas_saas import (
    PlanCreate, PlanUpdate, PlanRead, 
    TenantCreate, TenantRead, 
    SubscriptionUpdate, SubscriptionRead
)

router = APIRouter(
    prefix="/saas", 
    tags=["SaaS Management"]
)

# --- Endpoints para Planes ---

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


# --- Endpoints para Tenants ---

@router.post("/tenants", response_model=TenantRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("tenant:create"))])
def create_tenant(tenant_in: TenantCreate, saas_service: SaasService = Depends(get_saas_service)):
    try:
        return saas_service.create_tenant_and_admin(tenant_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/tenants/{tenant_id}", response_model=TenantRead, dependencies=[Depends(require_permission("tenant:read"))])
def get_tenant(tenant_id: uuid.UUID, saas_service: SaasService = Depends(get_saas_service)):
    return saas_service.get_tenant(tenant_id)


# --- Endpoints para Suscripciones ---

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
