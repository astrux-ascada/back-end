# /app/dependencies/permissions.py
"""
Dependencias de FastAPI para la autorización basada en permisos (RBAC granular).
"""
from fastapi import Depends, HTTPException, status
from typing import List

from app.dependencies.auth import get_current_active_user
from app.identity.models import User

def require_permission(permission_name: str):
    """
    Fábrica de dependencias que crea un validador para un permiso específico.

    Esta es la piedra angular de la seguridad granular. En lugar de verificar
    roles ('admin', 'supervisor'), verificamos capacidades ('asset:create', 'work_order:delete').

    Args:
        permission_name: El nombre del permiso requerido (ej: "asset:read").

    Returns:
        Una función de dependencia para ser usada en las rutas de FastAPI.
    """
    def _dependency(current_user: User = Depends(get_current_active_user)) -> None:
        """
        Valida si el usuario actual tiene el permiso requerido a través de alguno de sus roles.
        """
        if not check_user_permissions(current_user, [permission_name]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso requerido: '{permission_name}' no encontrado para este usuario."
            )

    return _dependency

def check_user_permissions(user: User, required_permissions: List[str]) -> bool:
    """
    Función helper que verifica si un usuario tiene al menos uno de los permisos de una lista.
    
    Args:
        user: El objeto de usuario a verificar.
        required_permissions: Una lista de nombres de permisos.

    Returns:
        True si el usuario tiene al menos uno de los permisos, False en caso contrario.
    """
    user_permissions = {perm.name for role in user.roles for perm in role.permissions}
    return any(perm in user_permissions for perm in required_permissions)
