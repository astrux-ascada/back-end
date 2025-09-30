# /app/identity/auth_service.py
"""
Servicio de negocio para la autenticación y gestión de sesiones de usuarios.
"""

import logging
import redis
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AuthenticationException, DuplicateRegistrationError
from app.core.security import create_access_token, verify_password
from app.identity.models import User
from app.identity.repository import UserRepository
from app.identity.schemas import UserCreate

logger = logging.getLogger("app.identity.service")


class AuthService:
    """Servicio de autenticación y sesión para usuarios de Astruxa."""

    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis_client = redis_client
        self.user_repo = UserRepository(self.db)

    def register_user(self, user_data: UserCreate) -> User:
        logger.info(f"Intento de registro para el email: {user_data.email}")
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            logger.warning(f"Conflicto: el email {user_data.email} ya está registrado.")
            raise DuplicateRegistrationError(email=user_data.email)
        new_user = self.user_repo.create(user_in=user_data)
        logger.info(f"Usuario registrado exitosamente: {new_user.email} (ID: {new_user.id})")
        return new_user

    def login_user(self, email: str, password: str) -> User:
        logger.info(f"Intento de login para el email: {email}")
        user = self.user_repo.get_by_email(email)
        if not user or not user.is_active or not verify_password(password, user.hashed_password):
            logger.warning(f"Intento de login fallido para el email: {email}")
            raise AuthenticationException("Email o contraseña incorrectos.")
        logger.info(f"Login exitoso para el usuario: {user.email} (ID: {user.id})")
        return user

    def create_user_session(self, user: User) -> str:
        access_token, jti = create_access_token(user)
        session_key = f"session:{jti}"
        session_duration_seconds = settings.JWT_EXPIRE_MINUTES * 60
        self.redis_client.set(session_key, str(user.id), ex=session_duration_seconds)
        logger.info(f"Sesión creada en Redis para el usuario {user.email} (JTI: {jti})")
        return access_token

    def logout_user(self, jti: str) -> None:
        session_key = f"session:{jti}"
        result = self.redis_client.delete(session_key)
        if result > 0:
            logger.info(f"Sesión cerrada exitosamente en Redis (JTI: {jti})")
        else:
            logger.warning(f"Se intentó cerrar una sesión no existente o ya expirada (JTI: {jti})")

    def logout_all_users(self) -> int:
        """
        Invalida TODAS las sesiones de usuario activas (recolector de sesiones).
        Busca y elimina todas las claves en Redis que coincidan con el patrón "session:*".
        
        Returns:
            El número de sesiones invalidadas.
        """
        logger.warning("Iniciando el proceso de limpieza de todas las sesiones de usuario activas.")
        session_keys = [key for key in self.redis_client.scan_iter("session:*")]
        
        if not session_keys:
            logger.info("No se encontraron sesiones activas para limpiar.")
            return 0

        # Usamos una pipeline para una operación de borrado masivo eficiente
        with self.redis_client.pipeline() as pipe:
            for key in session_keys:
                pipe.delete(key)
            pipe.execute()
            
        count = len(session_keys)
        logger.info(f"{count} sesiones de usuario han sido invalidadas exitosamente.")
        return count
