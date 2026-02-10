# /app/identity/auth_service.py
"""
Servicio de negocio para la autenticación, sesiones y 2FA de usuarios.
"""

import logging
import uuid
from typing import Dict, List, Optional

import redis
from sqlalchemy.orm import Session

from app.core import permissions as p
from app.core.config import settings
from app.core.error_messages import ErrorMessages
from app.core.exceptions import AuthenticationException, DuplicateRegistrationError, ConflictException, \
    NotFoundException, PermissionDeniedException, ValidationException
from app.core.security import create_access_token, verify_password, hash_password, \
    create_password_reset_token, verify_password_reset_token
from app.identity.models import User, Role, Permission
from app.identity.models.saas.subscription import Subscription, SubscriptionStatus
from app.identity.models.saas.tenant import Tenant
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

    def login_user(self, email: str, password: str) -> User:
        lockout_key = f"lockout:{email}"
        login_attempts_key = f"login_attempts:{email}"

        if self.redis_client.exists(lockout_key):
            raise PermissionDeniedException(ErrorMessages.AUTH_USER_LOCKED)

        user = self.user_repo.get_by_email(email)

        if not user or not user.is_active or not verify_password(password, user.hashed_password):
            current_attempts = self.redis_client.incr(login_attempts_key)
            self.redis_client.expire(login_attempts_key, settings.AUTH_LOCKOUT_DURATION_SECONDS)

            if current_attempts >= settings.AUTH_MAX_LOGIN_ATTEMPTS:
                self.redis_client.set(lockout_key, "locked", ex=settings.AUTH_LOCKOUT_DURATION_SECONDS)
                logger.warning(
                    f"Usuario {email} bloqueado por {settings.AUTH_LOCKOUT_DURATION_SECONDS}s por demasiados intentos de login.")
                raise PermissionDeniedException(ErrorMessages.AUTH_USER_LOCKED)

            raise AuthenticationException(ErrorMessages.AUTH_INVALID_CREDENTIALS)

        self.redis_client.delete(login_attempts_key)

        if user.tenant_id:
            subscription = (
                self.db.query(Subscription)
                .join(Tenant)
                .filter(Subscription.tenant_id == user.tenant_id)
                .first()
            )

            if not subscription or subscription.status in [SubscriptionStatus.CANCELED, SubscriptionStatus.EXPIRED]:
                logger.warning(
                    f"Login denegado para {user.email}: Suscripción {subscription.status if subscription else 'inexistente'}.")
                raise PermissionDeniedException(ErrorMessages.SUB_TENANT_SUSPENDED)

            if subscription.status == SubscriptionStatus.PAST_DUE:
                logger.warning(f"Login denegado para {user.email}: Suscripción PAST_DUE.")
                raise PermissionDeniedException(ErrorMessages.SUB_PAYMENT_REQUIRED)

        return user

    def create_user_session(self, user: User) -> str:
        active_session_key = f"active_session:{user.id}"
        old_jti = self.redis_client.get(active_session_key)
        if old_jti:
            self.redis_client.delete(f"session:{str(old_jti)}")
            logger.info(f"Sesión anterior {old_jti} para el usuario {user.id} invalidada.")

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

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_by_email(email)

    def list_users(self, tenant_id: uuid.UUID, skip: int, limit: int) -> List[User]:
        return self.user_repo.list_users(tenant_id=tenant_id, skip=skip, limit=limit)
        
    def list_all_users(self, requesting_user: User, skip: int, limit: int) -> List[User]:
        """
        Lista usuarios de la plataforma con lógica de negocio basada en el rol del solicitante.
        """
        # Determinar el rol del usuario que hace la petición
        is_super_admin = any(role.name == settings.SUPER_ADMIN_ROLE_NAME for role in requesting_user.roles)
        
        # Un PLATFORM_ADMIN no es un SUPER_ADMIN, pero tiene privilegios elevados
        is_platform_admin = any(role.name == "PLATFORM_ADMIN" for role in requesting_user.roles)

        if is_super_admin:
            # El Super Admin puede ver a todos, sin filtros.
            return self.user_repo.list_all_users(skip=skip, limit=limit)
        elif is_platform_admin:
            # El Platform Admin puede ver a todos excepto a los Super Admins.
            return self.user_repo.list_all_users(exclude_super_admins=True, skip=skip, limit=limit)
        else:
            # Si no es ninguno de los anteriores, no tiene permiso para esta acción.
            # La capa de API ya debería haberlo bloqueado con `require_permission`, pero esto es una defensa extra.
            raise PermissionDeniedException("No tienes permiso para listar todos los usuarios.")

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

    # Alias para compatibilidad con SaasService
    def create_user(self, email: str, name: str, password: str, tenant_id: uuid.UUID, roles: List[Role]) -> User:
        user_data = UserCreate(email=email, name=name, password=password)
        user = self.register_user(user_data, tenant_id)
        user.roles = roles
        self.db.commit()
        return user

    def create_tenant_admin_role(self, tenant_id: uuid.UUID) -> Role:
        """Crea el rol de administrador para un nuevo tenant."""
        role = Role(name=settings.TENANT_ADMIN_ROLE_NAME, description="Administrador del Tenant", tenant_id=tenant_id)

        # Asignar permisos por defecto
        permissions = self.db.query(Permission).filter(Permission.name.in_(p.DEFAULT_TENANT_ADMIN_PERMISSIONS)).all()
        role.permissions = permissions

        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def logout_user(self, jti: str) -> None:
        user_id = self.redis_client.get(f"session:{jti}")
        if user_id:
            self.redis_client.delete(f"active_session:{user_id}")
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

    def change_password(self, user: User, current_password: str, new_password: str):
        if not verify_password(current_password, user.hashed_password):
            raise AuthenticationException("La contraseña actual es incorrecta.")
        
        user.hashed_password = hash_password(new_password)
        self.db.commit()
        logger.info(f"Contraseña cambiada exitosamente para el usuario {user.email}.")

    async def forgot_password(self, email: str) -> Optional[str]:
        user = self.user_repo.get_by_email(email)
        if not user:
            # No revelamos si el usuario existe o no por seguridad
            logger.info(f"Solicitud de restablecimiento de contraseña para un email no registrado: {email}")
            return None
        
        # Generar token de restablecimiento
        reset_token = create_password_reset_token(email=user.email)
        
        # Aquí iría la lógica para enviar el correo electrónico
        # from app.core.email import send_password_reset_email
        # await send_password_reset_email(email_to=user.email, token=reset_token)
        
        return reset_token

    def reset_password(self, token: str, new_password: str) -> User:
        email = verify_password_reset_token(token)
        if not email:
            raise AuthenticationException("El token de restablecimiento es inválido o ha expirado.")
            
        user = self.user_repo.get_by_email(email)
        if not user:
            # Esto no debería ocurrir si el token es válido, pero es una salvaguarda
            raise NotFoundException("Usuario no encontrado.")
            
        user.hashed_password = hash_password(new_password)
        self.db.commit()
        logger.info(f"Contraseña restablecida exitosamente para el usuario {user.email}.")
        return user

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
