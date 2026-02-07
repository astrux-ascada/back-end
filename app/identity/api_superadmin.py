# /app/identity/api_superadmin.py
"""
API Router para operaciones de Super Administrador sobre la identidad.
"""
from typing import List
from fastapi import APIRouter, Depends

from app.dependencies.permissions import require_permission
from app.dependencies.services import get_auth_service
from app.identity.auth_service import AuthService
from app.identity.schemas import UserRead

router = APIRouter(
    prefix="/identity", 
    tags=["Super Admin - Identity"]
)

@router.get("/users/all", response_model=List[UserRead], dependencies=[Depends(require_permission("user:read_all"))])
def list_all_users(
    skip: int = 0,
    limit: int = 100,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    (Super Admin) Lista todos los usuarios de todos los tenants.
    """
    return auth_service.list_all_users(skip, limit)
