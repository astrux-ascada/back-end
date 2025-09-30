# /app/dependencies/auth.py
"""
Dependencias de FastAPI para la autenticación y autorización.

Define la lógica para proteger los endpoints, validando los tokens JWT
y las sesiones activas en Redis.
"""

import logging
import uuid
import redis
from typing import Dict, Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.database import get_db
from app.core.redis import get_redis_client
from app.core.security import verify_jwt_token
from app.core.exceptions import AuthenticationException
from app.identity.models import User
from app.identity.repository import UserRepository
from sqlalchemy.orm import Session

logger = logging.getLogger("app.dependency.auth")

bearer_scheme = HTTPBearer()

def get_current_token_payload(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    redis_client: redis.Redis = Depends(get_redis_client),
) -> Dict[str, Any]:
    """
    Valida el token JWT, comprueba la sesión en Redis y devuelve el payload del token.
    """
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
    """
    Dependencia principal para rutas protegidas. Obtiene el usuario a partir de un payload ya validado.
    """
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise AuthenticationException("Token inválido: falta el identificador del sujeto (sub).")

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise AuthenticationException("Token inválido: el identificador del sujeto no es un UUID válido.")

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)

    if not user or not user.is_active:
        raise AuthenticationException("Credenciales de autenticación no válidas o usuario inactivo.")

    return user

def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Dependencia que obtiene el usuario activo y verifica que sea administrador.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Se requieren permisos de administrador."
        )
    return current_user
