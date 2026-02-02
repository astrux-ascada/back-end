# /app/identity/api_roles.py
"""
API Router para la gestión de Roles y Permisos.
"""

import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_admin_user
from app.dependencies.services import get_role_service
from app.identity.role_service import RoleService
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
    """Obtiene una lista de todos los permisos disponibles en el sistema."""
    return role_service.list_permissions()


# --- Endpoints para Roles ---

@router.get("/roles", response_model=List[RoleRead])
def list_roles(role_service: RoleService = Depends(get_role_service)):
    """Obtiene una lista de todos los roles del sistema."""
    return role_service.list_roles()

@router.post("/roles", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(role_in: RoleCreate, role_service: RoleService = Depends(get_role_service)):
    """Crea un nuevo rol y le asigna los permisos especificados."""
    return role_service.create_role(role_in)

@router.get("/roles/{role_id}", response_model=RoleRead)
def get_role(role_id: uuid.UUID, role_service: RoleService = Depends(get_role_service)):
    """Obtiene los detalles de un rol específico por su ID."""
    return role_service.get_role(role_id)

@router.put("/roles/{role_id}", response_model=RoleRead)
def update_role(role_id: uuid.UUID, role_in: RoleUpdate, role_service: RoleService = Depends(get_role_service)):
    """Actualiza un rol existente (nombre, descripción y/o permisos)."""
    return role_service.update_role(role_id, role_in)

@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: uuid.UUID, role_service: RoleService = Depends(get_role_service)):
    """Elimina un rol del sistema."""
    role_service.delete_role(role_id)
    return None
