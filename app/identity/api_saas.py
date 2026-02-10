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
    PlanRead, TenantRead, TenantUpdate, TenantManagerAssignment, TenantCreate,
    TenantDeletionRequest
)
from app.auditing.schemas import ApprovalRequestRead

router = APIRouter(
    prefix="/saas", 
    tags=["SaaS Management"]
)

# --- Endpoints de Autogestión para Tenant Admins ---

@router.get("/me/tenant", response_model=TenantRead)
def get_my_tenant(
    current_user: User = Depends(get_current_active_user),
    saas_service: SaasService = Depends(get_saas_service)
):
    """
    Obtiene los detalles del tenant al que pertenece el usuario actual.
    """
    return saas_service.get_tenant_by_user(current_user)

@router.patch("/me/tenant", response_model=TenantRead)
def update_my_tenant(
    tenant_data: TenantUpdate,
    current_user: User = Depends(get_current_active_user),
    saas_service: SaasService = Depends(get_saas_service)
):
    """
    Actualiza los detalles del tenant al que pertenece el usuario actual.
    Requiere permisos de 'tenant:update'.
    """
    return saas_service.update_tenant_by_user(current_user, tenant_data)


# --- Endpoints para Gestión de Super Admin y Platform Admin ---

@router.post("/tenants", response_model=TenantRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("tenant:create"))])
def create_tenant(
    tenant_in: TenantCreate,
    saas_service: SaasService = Depends(get_saas_service)
):
    """
    (Admin) Crea un nuevo tenant en la plataforma.
    """
    return saas_service.create_tenant(tenant_in)

@router.get("/tenants", response_model=List[TenantRead], dependencies=[Depends(require_permission("tenant:read"))])
def list_tenants(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    saas_service: SaasService = Depends(get_saas_service)
):
    """
    (Admin) Lista tenants.
    - Super Admin (con tenant:read_all): ve todos los tenants.
    - Platform Admin: ve solo los tenants asignados a él.
    """
    return saas_service.list_tenants(current_user, skip, limit)

@router.get("/tenants/{tenant_id}", response_model=TenantRead, dependencies=[Depends(require_permission("tenant:read"))])
def get_tenant(
    tenant_id: uuid.UUID,
    saas_service: SaasService = Depends(get_saas_service)
):
    """
    (Admin) Obtiene los detalles de un tenant específico.
    """
    return saas_service.get_tenant(tenant_id)

@router.patch("/tenants/{tenant_id}", response_model=TenantRead, dependencies=[Depends(require_permission("tenant:update"))])
def update_tenant(
    tenant_id: uuid.UUID,
    tenant_in: TenantUpdate,
    saas_service: SaasService = Depends(get_saas_service)
):
    """
    (Admin) Actualiza los detalles de un tenant específico.
    """
    return saas_service.update_tenant(tenant_id, tenant_in)

@router.post("/tenants/{tenant_id}/delete", 
             status_code=status.HTTP_202_ACCEPTED, 
             response_model=ApprovalRequestRead,
             dependencies=[Depends(require_permission("tenant:delete"))])
def request_tenant_deletion(
    tenant_id: uuid.UUID,
    request_data: TenantDeletionRequest,
    current_user: User = Depends(get_current_active_user),
    saas_service: SaasService = Depends(get_saas_service)
):
    """
    (Admin) Inicia el proceso de eliminación de un tenant.
    - Si es Super Admin, el borrado es inmediato (y la respuesta será 204).
    - Si es Platform Admin, se crea una solicitud de aprobación.
    """
    result = saas_service.request_tenant_deletion(tenant_id, current_user, request_data.justification)
    if result is None:
        # Esto ocurre si el Super Admin realiza un borrado directo
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return result


@router.post("/tenants/{tenant_id}/assign-manager", response_model=TenantRead, dependencies=[Depends(require_permission("tenant:assign_manager"))])
def assign_manager(
    tenant_id: uuid.UUID,
    assignment: TenantManagerAssignment,
    saas_service: SaasService = Depends(get_saas_service)
):
    """(Super Admin) Asigna un gestor de cuenta (Platform Admin) a un tenant."""
    return saas_service.assign_manager_to_tenant(tenant_id, assignment.account_manager_id)
