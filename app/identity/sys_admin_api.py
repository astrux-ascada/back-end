# /app/identity/sys_admin_api.py
"""
API Router para la gestión de identidad a nivel de sistema (Super Admin).
"""
import logging
from typing import List

from fastapi import APIRouter, Depends, Query

from app.core.config import settings
from app.dependencies.auth import get_current_active_user
from app.dependencies.services import get_auth_service
from app.dependencies.permissions import require_permission
from app.identity.auth_service import AuthService
from app.identity.models import User
from app.identity.schemas import UserRead

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
    (Super Admin) Lista todos los usuarios de todos los tenants.
    - GLOBAL_SUPER_ADMIN: Ve a todos.
    - PLATFORM_ADMIN: Ve a todos excepto a los GLOBAL_SUPER_ADMIN.
    """
    users = auth_service.list_all_users(
        requesting_user=current_user, 
        skip=skip, 
        limit=limit
    )
    return users
