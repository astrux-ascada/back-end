# /app/dependencies/permissions.py
"""
Dependencias de FastAPI para la autorización basada en permisos (RBAC granular).
"""
from fastapi import Depends, HTTPException, status

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
        # Recorrer todos los roles asignados al usuario
        for role in current_user.roles:
            # Recorrer todos los permisos de cada rol
            for permission in role.permissions:
                if permission.name == permission_name:
                    # Si se encuentra el permiso, la validación es exitosa.
                    return

        # Si el bucle termina y no se encontró el permiso, lanzar un error.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permiso requerido: '{permission_name}' no encontrado para este usuario."
        )

    return _dependency
