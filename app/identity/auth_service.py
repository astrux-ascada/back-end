# /app/identity/auth_service.py
"""
Servicio de negocio para la autenticación, sesiones y 2FA de usuarios.
"""

import logging
import uuid
import redis
from typing import Dict, List
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AuthenticationException, DuplicateRegistrationError, ConflictException, NotFoundException
from app.core.security import create_access_token, verify_password
from app.identity.models import User
from app.identity.repository import UserRepository
from app.identity.schemas import UserCreate, UserUpdate
from app.identity.tfa_service import TfaService

logger = logging.getLogger("app.identity.service")


class AuthService:
    """Servicio de autenticación, sesión y 2FA para usuarios de Astruxa."""

    def __init__(self, db: Session, redis_client: redis.Redis, tfa_service: TfaService):
        self.db = db
        self.redis_client = redis_client
        self.tfa_service = tfa_service
        self.user_repo = UserRepository(self.db)

    def get_user_by_id(self, user_id: uuid.UUID) -> User:
        """Obtiene un usuario por su ID, lanzando una excepción si no se encuentra."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuario no encontrado.")
        return user

    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Devuelve una lista de usuarios."""
        return self.user_repo.list_users(skip=skip, limit=limit)

    def update_user(self, user_id: uuid.UUID, user_in: UserUpdate) -> User:
        """Actualiza la información de un usuario."""
        db_user = self.get_user_by_id(user_id)

        if user_in.email:
            existing_user = self.user_repo.get_by_email(user_in.email)
            if existing_user and existing_user.id != user_id:
                raise ConflictException("El correo electrónico ya está en uso por otro usuario.")

        return self.user_repo.update(db_user=db_user, user_in=user_in)

    def delete_user(self, user_id: uuid.UUID) -> User:
        """Marca a un usuario como inactivo (soft delete)."""
        db_user = self.get_user_by_id(user_id)
        return self.user_repo.soft_delete(db_user)

    # --- Métodos existentes ---
    def register_user(self, user_data: UserCreate) -> User:
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise DuplicateRegistrationError(email=user_data.email)
        new_user = self.user_repo.create(user_in=user_data)
        return new_user

    def login_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user or not user.is_active or not verify_password(password, user.hashed_password):
            raise AuthenticationException("Email o contraseña incorrectos.")
        return user

    def create_user_session(self, user: User) -> str:
        access_token, jti = create_access_token(user)
        session_key = f"session:{jti}"
        session_duration_seconds = settings.JWT_EXPIRE_MINUTES * 60
        self.redis_client.set(session_key, str(user.id), ex=session_duration_seconds)
        return access_token

    def logout_user(self, jti: str) -> None:
        self.redis_client.delete(f"session:{jti}")

    def logout_all_users(self) -> int:
        session_keys = [key for key in self.redis_client.scan_iter("session:*")]
        if not session_keys:
            return 0
        with self.redis_client.pipeline() as pipe:
            for key in session_keys:
                pipe.delete(key)
            pipe.execute()
        return len(session_keys)

    # --- Métodos 2FA ---
    def setup_tfa(self, user: User) -> Dict[str, str]:
        """Genera y guarda un nuevo secreto 2FA para un usuario."""
        if user.is_tfa_enabled:
            raise ConflictException("El 2FA ya está habilitado para este usuario.")
        
        secret = self.tfa_service.generate_secret()
        user.tfa_secret = secret
        self.db.commit()
        
        return {
            "setup_key": secret,
            "otpauth_url": self.tfa_service.get_otpauth_url(secret, user.email)
        }

    def enable_tfa(self, user: User, token: str) -> bool:
        """Verifica el token inicial y habilita el 2FA para el usuario."""
        if not user.tfa_secret:
            raise ConflictException("El proceso de configuración de 2FA no se ha iniciado.")

        if self.tfa_service.verify_token(user.tfa_secret, token):
            user.is_tfa_enabled = True
            self.db.commit()
            logger.info(f"2FA habilitado exitosamente para el usuario: {user.email}")
            return True
        
        logger.warning(f"Intento fallido de habilitar 2FA para el usuario: {user.email}")
        return False

    def verify_tfa_token(self, user: User, token: str) -> bool:
        """Verifica un token 2FA para una operación crítica."""
        if not user.is_tfa_enabled or not user.tfa_secret:
            logger.error(f"Intento de verificar 2FA para el usuario {user.email} sin 2FA habilitado.")
            return False
        
        return self.tfa_service.verify_token(user.tfa_secret, token)
