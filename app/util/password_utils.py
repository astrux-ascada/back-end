# /app/utils/password_utils.py
"""
Módulo de utilidad para todo lo relacionado con el manejo de contraseñas.
"""
from passlib.context import CryptContext

# Creamos el contexto aquí, en un único lugar.
# Si en el futuro queremos cambiar a argon2, solo lo cambiamos aquí.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña plana contra su hash."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hashea una contraseña plana."""
    return pwd_context.hash(password)