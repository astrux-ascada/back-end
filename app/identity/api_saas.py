# /app/identity/api_saas.py
"""
API Router para la gestión del modelo de negocio SaaS (Planes, Tenants, etc.).
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException

from app.dependencies.permissions import require_permission
from app.dependencies.services import get_saas_service
from app.dependencies.auth import get_current_active_user
from app.identity.models import User
from app.identity.service_saas import SaasService
from app.identity.schemas_saas import (
    PlanRead, TenantRead, TenantUpdate, TenantManagerAssignment
)

router = APIRouter(
    prefix="/saas", 
    tags=["SaaS Management"]
)

# ... (endpoints de autogestión y planes) ...

# --- Endpoints para Gestión de Super Admin y Platform Admin ---

@router.get("/tenants", response_model=List[TenantRead], dependencies=[Depends(require_permission("tenant:read"))])
def list_tenants(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    saas_service: SaasService = Depends(get_saas_service)
):
    """
    Lista tenants.
    - Super Admin (con tenant:read_all): ve todos los tenants.
    - Platform Admin: ve solo los tenants asignados a él.
    """
    return saas_service.list_tenants(current_user, skip, limit)

@router.post("/tenants/{tenant_id}/assign-manager", response_model=TenantRead, dependencies=[Depends(require_permission("tenant:assign_manager"))])
def assign_manager(
    tenant_id: uuid.UUID,
    assignment: TenantManagerAssignment,
    saas_service: SaasService = Depends(get_saas_service)
):
    """(Super Admin) Asigna un gestor de cuenta (Platform Admin) a un tenant."""
    return saas_service.assign_manager_to_tenant(tenant_id, assignment.account_manager_id)

# ... (resto de endpoints de gestión de tenants) ...
