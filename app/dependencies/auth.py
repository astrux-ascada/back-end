# /app/dependencies/auth.py
"""
Dependencias de FastAPI para la autenticación y autorización.
"""

import logging
import uuid
import redis
from typing import Dict, Any

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
        raise AuthenticationException("Token inválido o expirado.")

    jti = payload.get("jti")
    if not jti:
        raise AuthenticationException("Token inválido: falta el identificador de sesión (jti).")

    session_key = f"session:{jti}"
    if not redis_client.exists(session_key):
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

    user = db.query(User).options(joinedload(User.roles).joinedload(Role.permissions)).filter(User.id == user_id).first()

    if not user or not user.is_active:
        raise AuthenticationException("Credenciales de autenticación no válidas o usuario inactivo.")

    return user

def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Dependencia que obtiene el usuario activo y verifica que tenga el rol 'Admin' o 'Super User'."""
    # Nombres de roles estandarizados (insensible a mayúsculas)
    admin_roles = ["admin", "super user"]
    user_roles = [role.name.lower() for role in current_user.roles]
    
    if not any(role_name in user_roles for role_name in admin_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Se requieren permisos de Administrador o superiores."
        )
    return current_user

def get_current_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Dependencia que obtiene el usuario activo y verifica que tenga el rol 'Super User'."""
    user_roles = [role.name.lower() for role in current_user.roles]
    if "super user" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Se requieren permisos de Super User."
        )
    return current_user
