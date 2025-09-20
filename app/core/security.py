from jose import JWTError, jwt
from passlib.context import CryptContext

# --- CONFIGURACIÓN DE SEGURIDAD ---
SECRET_KEY = "super-secret-key-industrial-2025"  # ¡Debería estar en una variable de entorno!
ALGORITHM = "HS256"

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
def create_jwt_token(data: dict) -> str:
    """Crea un nuevo token JWT."""
    return jwt.encode(data.copy(), SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str) -> dict | None:
    """Verifica un token JWT y devuelve su payload si es válido."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
