# /app/dependencies/auth.py
"""
Dependencias de FastAPI para la autenticación y autorización.
"""

import logging
import uuid
import redis
from typing import Dict, Any, List
from functools import wraps

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.database import get_db
from app.core.redis import get_redis_client
from app.core.security import verify_jwt_token
from app.core.exceptions import AuthenticationException
from app.identity.models import User, Role
from sqlalchemy.orm import Session, joinedload

logger = logging.getLogger("app.dependency.auth")

bearer_scheme = HTTPBearer()

def get_current_token_payload(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    redis_client: redis.Redis = Depends(get_redis_client),
) -> Dict[str, Any]:
    payload = verify_jwt_token(token.credentials)
    if not payload:
        logger.warning("Token JWT inválido o expirado.")
        raise AuthenticationException("Token inválido o expirado.")

    jti = payload.get("jti")
    if not jti:
        logger.warning("Token JWT sin JTI.")
        raise AuthenticationException("Token inválido: falta el identificador de sesión (jti).")

    session_key = f"session:{jti}"
    if not redis_client.exists(session_key):
        logger.warning(f"Sesión no encontrada en Redis para JTI: {jti}. Posible sesión expirada o revocada.")
        raise AuthenticationException("La sesión ha sido cerrada o es inválida.")

    return payload

def get_current_active_user(
    payload: Dict[str, Any] = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
) -> User:
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise AuthenticationException("Token inválido: falta el identificador del sujeto (sub).")

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise AuthenticationException("Token inválido: el identificador del sujeto no es un UUID válido.")

    user = db.query(User).options(joinedload(User.roles)).filter(User.id == user_id).first()

    if not user:
        logger.warning(f"Usuario con ID {user_id} no encontrado en la base de datos.")
        raise AuthenticationException("Credenciales de autenticación no válidas.")
        
    if not user.is_active:
        logger.warning(f"Usuario {user.email} está inactivo.")
        raise AuthenticationException("Usuario inactivo.")

    return user

# --- NUEVA DEPENDENCIA DE ROLES GENÉRICA ---
def require_role(allowed_roles: List[str]):
    """
    Factoría de dependencias que crea un validador de roles.
    Permite el acceso si el usuario tiene CUALQUIERA de los roles en `allowed_roles`.
    Siempre permite el acceso a 'ADMINISTRATOR' y 'SUPERUSER'.
    """
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        # Normalizar roles para comparación insensible a mayúsculas/minúsculas
        user_roles = {role.name.upper() for role in current_user.roles}
        
        # Permitir siempre a los administradores y superusuarios
        if "ADMINISTRATOR" in user_roles or "SUPERUSER" in user_roles:
            return current_user
            
        # Verificar si el usuario tiene alguno de los roles permitidos
        if not any(role.upper() in user_roles for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker

# --- Dependencias antiguas (pueden ser reemplazadas o mantenidas por conveniencia) ---

def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Dependencia que obtiene el usuario activo y verifica que tenga el rol 'ADMINISTRATOR' o 'SUPERUSER'."""
    user_roles = {role.name.upper() for role in current_user.roles}
    if "ADMINISTRATOR" not in user_roles and "SUPERUSER" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Se requieren permisos de Administrador o superiores."
        )
    return current_user

def get_current_superuser(current_user: User = Depends(get_current_active_user)) -> User:
    """Dependencia que obtiene el usuario activo y verifica que tenga el rol 'SUPERUSER'."""
    user_roles = {role.name.upper() for role in current_user.roles}
    if "SUPERUSER" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Se requieren permisos de Super User."
        )
    return current_user
