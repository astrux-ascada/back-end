# /app/core/security.py
"""
Módulo central de seguridad.

Contiene la lógica para:
- Hashing y verificación de contraseñas.
- Creación y decodificación de JSON Web Tokens (JWT).
- Dependencias de FastAPI para la autenticación.
"""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Tuple

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.identity.models import User

# --- Configuración de Hashing de Contraseñas ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña en texto plano contra su hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Genera el hash de una contraseña en texto plano."""
    return pwd_context.hash(password)


# --- Lógica de JSON Web Tokens (JWT) ---

def create_access_token(user: User) -> Tuple[str, str]:
    """
    Genera un nuevo token de acceso JWT para un usuario.

    Returns:
        Una tupla con (access_token, jti).
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )
    jti = str(uuid.uuid4())
    
    # Comprobar si el usuario tiene el rol de Super Admin
    is_admin = any(role.name == settings.SUPER_ADMIN_ROLE_NAME for role in user.roles)
    
    token_payload = {
        "sub": str(user.id),
        "email": user.email,
        "is_admin": is_admin,
        "exp": expire,
        "jti": jti,  # JWT ID: Identificador único para este token
    }
    
    access_token = jwt.encode(
        token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    
    return access_token, jti


def verify_jwt_token(token: str) -> dict[str, Any] | None:
    """Verifica un token JWT y devuelve su payload si es válido."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        return None
