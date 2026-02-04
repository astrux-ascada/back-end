# /app/identity/auth_service.py
"""
Servicio de negocio para la autenticación, sesiones y 2FA de usuarios.
"""

import logging
import uuid
import redis
from typing import Dict, List, Optional # Añadir Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AuthenticationException, DuplicateRegistrationError, ConflictException, NotFoundException, PermissionDeniedException
from app.core.security import create_access_token, verify_password
from app.identity.models import User
from app.identity.models.saas.tenant import Tenant
from app.identity.models.saas.subscription import Subscription, SubscriptionStatus
from app.identity.models.saas.plan import Plan
from app.identity.repository import UserRepository
from app.identity.schemas import UserCreate, UserUpdate
from app.identity.tfa_service import TfaService
from app.core.error_messages import ErrorMessages

logger = logging.getLogger("app.identity.service")

# --- Constantes para Seguridad de Sesión ---
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_SECONDS = 900  # 15 minutos


class AuthService:
    """Servicio de autenticación, sesión y 2FA para usuarios de Astruxa."""

    def __init__(self, db: Session, redis_client: redis.Redis, tfa_service: TfaService):
        self.db = db
        self.redis_client = redis_client
        self.tfa_service = tfa_service
        self.user_repo = UserRepository(self.db)

    def login_user(self, email: str, password: str) -> User:
        lockout_key = f"lockout:{email}"
        login_attempts_key = f"login_attempts:{email}"

        # 1. Verificar si el usuario está bloqueado
        if self.redis_client.exists(lockout_key):
            raise PermissionDeniedException(ErrorMessages.AUTH_USER_LOCKED)

        user = self.user_repo.get_by_email(email)
        
        # 2. Verificar credenciales básicas
        if not user or not user.is_active or not verify_password(password, user.hashed_password):
            # Incrementar contador de intentos fallidos
            current_attempts = self.redis_client.incr(login_attempts_key)
            self.redis_client.expire(login_attempts_key, LOCKOUT_DURATION_SECONDS)

            if current_attempts >= MAX_LOGIN_ATTEMPTS:
                self.redis_client.set(lockout_key, "locked", ex=LOCKOUT_DURATION_SECONDS)
                logger.warning(f"Usuario {email} bloqueado por {LOCKOUT_DURATION_SECONDS}s por demasiados intentos de login.")
                raise PermissionDeniedException(ErrorMessages.AUTH_USER_LOCKED)
            
            raise AuthenticationException(ErrorMessages.AUTH_INVALID_CREDENTIALS)
        
        # 3. Si el login es exitoso, resetear el contador de intentos
        self.redis_client.delete(login_attempts_key)
        
        # 4. Verificar estado del Tenant y Suscripción (Gatekeeper)
        if user.tenant_id:
            subscription = (
                self.db.query(Subscription)
                .join(Tenant)
                .filter(Subscription.tenant_id == user.tenant_id)
                .first()
            )

            if not subscription or subscription.status in [SubscriptionStatus.CANCELED, SubscriptionStatus.EXPIRED]:
                logger.warning(f"Login denegado para {user.email}: Suscripción {subscription.status if subscription else 'inexistente'}.")
                raise PermissionDeniedException(ErrorMessages.SUB_TENANT_SUSPENDED)
            
            if subscription.status == SubscriptionStatus.PAST_DUE:
                logger.warning(f"Login denegado para {user.email}: Suscripción PAST_DUE.")
                raise PermissionDeniedException(ErrorMessages.SUB_PAYMENT_REQUIRED)

        return user

    def create_user_session(self, user: User) -> str:
        # --- Control de Concurrencia ---
        active_session_key = f"active_session:{user.id}"
        old_jti = self.redis_client.get(active_session_key)
        if old_jti:
            self.redis_client.delete(f"session:{old_jti.decode()}")
            logger.info(f"Sesión anterior {old_jti.decode()} para el usuario {user.id} invalidada.")

        access_token, jti = create_access_token(user)
        session_key = f"session:{jti}"
        session_duration_seconds = settings.JWT_EXPIRE_MINUTES * 60
        
        self.redis_client.set(session_key, str(user.id), ex=session_duration_seconds)
        self.redis_client.set(active_session_key, jti, ex=session_duration_seconds)
        
        return access_token

    def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(ErrorMessages.AUTH_USER_NOT_FOUND)
        return user

    def list_users(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[User]:
        return self.user_repo.list_users(tenant_id=tenant_id, skip=skip, limit=limit)

    def update_user(self, user_id: uuid.UUID, user_in: UserUpdate) -> User:
        db_user = self.get_user_by_id(user_id)
        if user_in.email:
            existing_user = self.user_repo.get_by_email(user_in.email)
            if existing_user and existing_user.id != user_id:
                raise ConflictException(ErrorMessages.AUTH_EMAIL_ALREADY_EXISTS)
        return self.user_repo.update(db_user=db_user, user_in=user_in)

    def delete_user(self, user_id: uuid.UUID) -> User:
        db_user = self.get_user_by_id(user_id)
        return self.user_repo.soft_delete(db_user)

    def register_user(self, user_data: UserCreate, tenant_id: Optional[uuid.UUID] = None) -> User:
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise DuplicateRegistrationError(email=user_data.email)
        new_user = self.user_repo.create(user_in=user_data, tenant_id=tenant_id)
        return new_user

    def logout_user(self, jti: str) -> None:
        user_id = self.redis_client.get(f"session:{jti}")
        if user_id:
            self.redis_client.delete(f"active_session:{user_id.decode()}")
        self.redis_client.delete(f"session:{jti}")

    def logout_all_users(self, tenant_id: Optional[uuid.UUID] = None) -> int:
        session_keys = [key for key in self.redis_client.scan_iter("session:*")]
        active_session_keys = [key for key in self.redis_client.scan_iter("active_session:*")]
        if not session_keys and not active_session_keys:
            return 0
        
        if tenant_id:
            logger.warning("Logout de todas las sesiones por tenant_id no implementado completamente en Redis.")
            return 0
        
        with self.redis_client.pipeline() as pipe:
            for key in session_keys + active_session_keys:
                pipe.delete(key)
            pipe.execute()
        return len(session_keys)

    def setup_tfa(self, user: User) -> Dict[str, str]:
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
        if not user.is_tfa_enabled or not user.tfa_secret:
            logger.error(f"Intento de verificar 2FA para el usuario {user.email} sin 2FA habilitado.")
            return False
        return self.tfa_service.verify_token(user.tfa_secret, token)
