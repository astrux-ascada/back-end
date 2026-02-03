# /app/identity/api_roles.py
"""
API Router para la gestión de Roles y Permisos.
"""

import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_admin_user
from app.dependencies.services import get_role_service, get_audit_service
from app.dependencies.tenant import get_tenant_id
from app.identity.role_service import RoleService
from app.auditing.service import AuditService
from app.identity.models import User
from app.identity.schemas import RoleCreate, RoleUpdate, RoleRead, PermissionRead

logger = logging.getLogger(__name__)

# Todos los endpoints en este router requerirán autenticación de administrador.
router = APIRouter(
    prefix="/identity", 
    tags=["Identity Management"], 
    dependencies=[Depends(get_current_admin_user)]
)


# --- Endpoints para Permisos ---

@router.get("/permissions", response_model=List[PermissionRead])
def list_permissions(role_service: RoleService = Depends(get_role_service)):
    """Obtiene una lista de todos los permisos disponibles en el sistema (Globales)."""
    return role_service.list_permissions()


# --- Endpoints para Roles ---

@router.get("/roles", response_model=List[RoleRead])
def list_roles(
    role_service: RoleService = Depends(get_role_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """Obtiene una lista de todos los roles del tenant actual."""
    return role_service.list_roles(tenant_id)

@router.post("/roles", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(
    role_in: RoleCreate, 
    role_service: RoleService = Depends(get_role_service),
    audit_service: AuditService = Depends(get_audit_service),
    current_user: User = Depends(get_current_admin_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """Crea un nuevo rol para el tenant actual y le asigna permisos."""
    new_role = role_service.create_role(role_in, tenant_id)
    
    audit_service.log_operation(
        user=current_user,
        action="CREATE_ROLE",
        entity=new_role,
        details={"name": new_role.name}
    )
    return new_role

@router.get("/roles/{role_id}", response_model=RoleRead)
def get_role(
    role_id: uuid.UUID, 
    role_service: RoleService = Depends(get_role_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """Obtiene los detalles de un rol específico del tenant actual."""
    return role_service.get_role(role_id, tenant_id)

@router.put("/roles/{role_id}", response_model=RoleRead)
def update_role(
    role_id: uuid.UUID, 
    role_in: RoleUpdate, 
    role_service: RoleService = Depends(get_role_service),
    audit_service: AuditService = Depends(get_audit_service),
    current_user: User = Depends(get_current_admin_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """Actualiza un rol existente del tenant (nombre, descripción y/o permisos)."""
    updated_role = role_service.update_role(role_id, role_in, tenant_id)
    
    audit_service.log_operation(
        user=current_user,
        action="UPDATE_ROLE",
        entity=updated_role,
        details=role_in.model_dump(exclude_unset=True)
    )
    return updated_role

@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: uuid.UUID, 
    role_service: RoleService = Depends(get_role_service),
    audit_service: AuditService = Depends(get_audit_service),
    current_user: User = Depends(get_current_admin_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """Elimina un rol del tenant."""
    deleted_role = role_service.delete_role(role_id, tenant_id)
    
    audit_service.log_operation(
        user=current_user,
        action="DELETE_ROLE",
        entity=deleted_role
    )
    return None
