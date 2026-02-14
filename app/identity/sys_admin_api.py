# /app/identity/sys_admin_api.py
"""
API Router para la gestión de identidad a nivel de sistema (Super Admin / Platform Admin).
"""
import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.core.config import settings
from app.dependencies.auth import get_current_active_user
from app.dependencies.services import get_auth_service
from app.dependencies.permissions import require_permission
from app.identity.auth_service import AuthService
from app.identity.models import User
from app.identity.schemas import UserRead, UserCreateSys, UserUpdateSys

logger = logging.getLogger("app.identity.sys_admin_api")

# Este router se montará bajo /api/v1/sys-mgt/identity
router = APIRouter(tags=["Super Admin - Identity"])


@router.get(
    "/users/all", 
    response_model=List[UserRead], 
    dependencies=[Depends(require_permission("user:read_all"))]
)
def list_all_users(
    skip: int = Query(default=settings.DEFAULT_PAGINATION_SKIP, ge=0),
    limit: int = Query(default=settings.DEFAULT_PAGINATION_LIMIT, ge=1, le=1000),
    auth_service: AuthService = Depends(get_auth_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    (Admin) Lista todos los usuarios de la plataforma.
    - GLOBAL_SUPER_ADMIN: Ve a todos.
    - PLATFORM_ADMIN: Ve a todos excepto a los GLOBAL_SUPER_ADMIN.
    """
    users = auth_service.list_all_users(
        requesting_user=current_user, 
        skip=skip, 
        limit=limit
    )
    return users

@router.get(
    "/users/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_permission("user:read_all"))]
)
def get_user(
    user_id: uuid.UUID,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    (Admin) Obtiene los detalles completos de un usuario específico por su ID.
    Incluye roles, tenant y sectores asignados.
    """
    return auth_service.get_user_by_id(user_id)

@router.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("user:create_any"))]
)
def create_user(
    user_in: UserCreateSys,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    (Admin) Crea un nuevo usuario en la plataforma.
    Puede ser asignado a un tenant o ser un usuario global (sin tenant_id).
    """
    new_user = auth_service.create_any_user(user_in)
    return new_user

@router.put(
    "/users/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_permission("user:update_any"))]
)
def update_user(
    user_id: uuid.UUID,
    user_in: UserUpdateSys,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    (Admin) Actualiza un usuario por su ID.
    - PLATFORM_ADMIN no puede editar a GLOBAL_SUPER_ADMIN.
    - Nadie puede editarse a sí mismo por esta vía.
    """
    updated_user = auth_service.update_any_user(
        requesting_user=current_user,
        user_id_to_update=user_id,
        data=user_in
    )
    return updated_user

@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("user:delete_any"))]
)
def delete_user(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """

    (Admin) Elimina (soft delete) un usuario por su ID.
    - PLATFORM_ADMIN no puede eliminar a GLOBAL_SUPER_ADMIN.
    - Nadie puede eliminarse a sí mismo.
    """
    auth_service.delete_any_user(
        requesting_user=current_user,
        user_id_to_delete=user_id
    )
    return None
