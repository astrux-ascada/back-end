import os
from datetime import datetime, timedelta
import uuid
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

# --- CONFIGURACIÓN DE SEGURIDAD (desde variables de entorno) ---

# La clave secreta para firmar los JWT. ¡Es crucial que sea secreta y compleja!
# La aplicación no se iniciará si esta variable no está definida.
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No se ha definido la variable de entorno SECRET_KEY")

ALGORITHM = "HS256"
# El tiempo de vida del token de acceso, en minutos.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


# --- CONTEXTO DE HASHING DE CONTRASEÑAS ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- FUNCIONES DE CONTRASEÑA ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que una contraseña en texto plano coincide con un hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña en texto plano."""
    return pwd_context.hash(password)


# --- FUNCIONES DE TOKEN JWT ---
def create_access_token(subject: uuid.UUID, expires_delta: timedelta | None = None) -> str:
    """Crea un nuevo token de acceso JWT."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token: str) -> dict[str, Any] | None:
    """Verifica un token JWT y devuelve su payload si es válido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
