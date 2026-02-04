# /app/identity/api_roles.py
"""
API Router para la gestión de Roles y Permisos.
"""
import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status

from app.dependencies.permissions import require_permission
from app.dependencies.services import get_role_service, get_audit_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.auth import get_current_active_user # Importar la dependencia
from app.identity.role_service import RoleService
from app.auditing.service import AuditService
from app.identity.models import User
from app.identity.schemas import RoleCreate, RoleUpdate, RoleRead, PermissionRead

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/identity", 
    tags=["Identity Management"]
)

# --- Endpoints para Permisos ---

@router.get("/permissions", response_model=List[PermissionRead], dependencies=[Depends(require_permission("permission:read"))])
def list_permissions(role_service: RoleService = Depends(get_role_service)):
    return role_service.list_permissions()


# --- Endpoints para Roles ---

@router.get("/roles", response_model=List[RoleRead], dependencies=[Depends(require_permission("role:read"))])
def list_roles(
    role_service: RoleService = Depends(get_role_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    return role_service.list_roles(tenant_id)

@router.post("/roles", response_model=RoleRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("role:create"))])
def create_role(
    role_in: RoleCreate, 
    role_service: RoleService = Depends(get_role_service),
    audit_service: AuditService = Depends(get_audit_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    new_role = role_service.create_role(role_in, tenant_id)
    audit_service.log_operation(user=current_user, action="CREATE_ROLE", entity=new_role)
    return new_role

@router.get("/roles/{role_id}", response_model=RoleRead, dependencies=[Depends(require_permission("role:read"))])
def get_role(
    role_id: uuid.UUID, 
    role_service: RoleService = Depends(get_role_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    return role_service.get_role(role_id, tenant_id)

@router.put("/roles/{role_id}", response_model=RoleRead, dependencies=[Depends(require_permission("role:update"))])
def update_role(
    role_id: uuid.UUID, 
    role_in: RoleUpdate, 
    role_service: RoleService = Depends(get_role_service),
    audit_service: AuditService = Depends(get_audit_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    updated_role = role_service.update_role(role_id, role_in, tenant_id)
    audit_service.log_operation(user=current_user, action="UPDATE_ROLE", entity=updated_role)
    return updated_role

@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permission("role:delete"))])
def delete_role(
    role_id: uuid.UUID, 
    role_service: RoleService = Depends(get_role_service),
    audit_service: AuditService = Depends(get_audit_service),
    current_user: User = Depends(get_current_active_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    deleted_role = role_service.delete_role(role_id, tenant_id)
    audit_service.log_operation(user=current_user, action="DELETE_ROLE", entity=deleted_role)
    return None
