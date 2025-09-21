# /app/core/security.py
"""
Módulo central de seguridad.

Contiene la lógica para:
- Hashing y verificación de contraseñas.
- Creación y decodificación de JSON Web Tokens (JWT).
- Dependencias de FastAPI para la autenticación.
"""
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt  # Usamos PyJWT de forma consistente
from passlib.context import CryptContext

from app.core.config import settings
# --- MEJORA: Importamos el nuevo modelo User ---
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

# --- MEJORA: La función ahora trabaja con el modelo User ---
def create_access_token(user: User) -> str:
    """
    Genera un nuevo token de acceso JWT para un usuario.
    El token incluye el ID del usuario como "subject" y otros datos relevantes.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )
    token_payload = {
        "sub": str(user.id),  # Usamos el nuevo ID de tipo UUID
        "email": user.email,
        "is_admin": user.is_admin,
        "exp": expire,
    }
    return jwt.encode(
        token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )


# --- MEJORA: Corregido para usar PyJWT de forma consistente ---
def verify_jwt_token(token: str) -> dict[str, Any] | None:
    """Verifica un token JWT y devuelve su payload si es válido."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:  # Captura cualquier error de PyJWT (expirado, inválido, etc.)
        return None
