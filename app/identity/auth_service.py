# /app/identity/auth_service.py
"""
Servicio de negocio para la autenticación de usuarios.

Contiene la lógica para registrar y autenticar usuarios, orquestando
la interacción entre la capa de la API, el repositorio y el core de seguridad.
"""

import logging

from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationException, DuplicateRegistrationError
from app.core.security import verify_password
from app.identity.models import User
from app.identity.repository import UserRepository
from app.identity.schemas import UserCreate

logger = logging.getLogger("app.identity.service")


class AuthService:
    """Servicio de autenticación para usuarios de Astruxa."""

    def __init__(self, db: Session):
        """Inicializa el servicio con una sesión de BD y el repositorio de usuarios."""
        self.db = db
        self.user_repo = UserRepository(self.db)

    def register_user(self, user_data: UserCreate) -> User:
        """
        Registra un nuevo usuario en el sistema.

        1. Verifica si el email ya existe para evitar duplicados.
        2. Si no existe, crea el usuario a través del repositorio.
        """
        logger.info(f"Intento de registro para el email: {user_data.email}")
        existing_user = self.user_repo.get_by_email(user_data.email)

        if existing_user:
            logger.warning(f"Conflicto: el email {user_data.email} ya está registrado.")
            raise DuplicateRegistrationError(email=user_data.email)

        # El repositorio se encarga de hashear la contraseña y crear el usuario.
        new_user = self.user_repo.create(user_in=user_data)

        logger.info(f"Usuario registrado exitosamente: {new_user.email} (ID: {new_user.id})")
        return new_user

    def login_user(self, email: str, password: str) -> User:
        """
        Autentica a un usuario.

        1. Busca al usuario por email.
        2. Si existe y la contraseña es correcta, devuelve el objeto User.
        3. En cualquier otro caso, lanza una excepción.
        """
        logger.info(f"Intento de login para el email: {email}")
        user = self.user_repo.get_by_email(email)

        if not user or not user.is_active or not verify_password(password, user.hashed_password):
            logger.warning(f"Intento de login fallido para el email: {email}")
            raise AuthenticationException("Email o contraseña incorrectos.")

        logger.info(f"Login exitoso para el usuario: {user.email} (ID: {user.id})")
        return user
