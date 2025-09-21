# /app/dependencies/auth.py (Versión Refactorizada)

import logging
import uuid
from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.orm import Session

# --- MEJORA: Importamos nuestras excepciones personalizadas ---
from app.core.exceptions import AuthenticationException 
from app.core.config import settings, get_db
from app.models import client as client_model
from app.repositories.client import ClientRepository

# Usar HTTP Bearer para extraer el token del encabezado "Authorization".
security = HTTPBearer()
# --- NUEVO: Un segundo Bearer que no lanza error si el token no está presente ---
security_optional = HTTPBearer(auto_error=False)
logger = logging.getLogger("app.dependency.auth")


def _get_client_from_token_credentials(
    token: Optional[HTTPAuthorizationCredentials], db: Session
) -> client_model.Client:
    """
    Lógica central para validar un token y devolver un cliente.

    Si alguna validación falla, lanza una AuthenticationException que es manejada
    por el sistema de excepciones global para devolver un error 401 consistentes.
    """
    # --- MEJORA: Usamos un único bloque try/except para capturar todos los errores
    # de validación del token y los convertimos en nuestra excepción estándar. ---
    try:
        if not token:
            raise AuthenticationException("No se proporcionó token de autenticación.")

        payload = jwt.decode(
            token.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        # --- CORRECCIÓN CRÍTICA (1): Usamos el claim 'sub' (subject) como es el estándar JWT ---
        client_uuid_str = payload.get("sub")
        if client_uuid_str is None:
            raise AuthenticationException(
                "Token inválido: falta el identificador del sujeto (sub)."
            )

        # --- CORRECCIÓN CRÍTICA (2): Convertimos el string a un objeto UUID ---
        client_uuid = uuid.UUID(client_uuid_str)

    except jwt.ExpiredSignatureError:
        logger.warning("Intento de acceso con token expirado.")
        raise AuthenticationException("El token ha expirado.")
    except (jwt.InvalidTokenError, ValueError):
        # Capturamos errores de JWT (firma, formato) y errores de conversión de UUID.
        logger.warning("Intento de acceso con token inválido o malformado.")
        raise AuthenticationException("Token inválido o malformado.")

    # Una vez validado el token, buscamos al cliente en la base de datos.
    client_repo = ClientRepository(db)
    # --- CORRECCIÓN CRÍTICA (3): Usamos el método correcto del repositorio: get_by_uuid ---
    client = client_repo.get_by_uuid(client_uuid)

    # Verificamos que el cliente exista y esté activo.
    if client is None:
        # No revelamos que el cliente no existe, simplemente que la autenticación falló.
        logger.error(
            f"Autenticación fallida: el cliente con UUID {client_uuid} del token no existe en la BD."
        )
        raise AuthenticationException("Credenciales de autenticación no válidas.")

    if not client.is_active:
        logger.warning(f"Intento de login para cuenta inactiva: {client.email}")
        raise AuthenticationException("La cuenta de usuario está inactiva.")

    return client


def get_current_active_client(
    token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
) -> client_model.Client:
    """
    Dependencia para obtener el cliente autenticado y activo.
    Lanza un error 401 si el token es inválido, no está presente o el usuario no está activo.
    USAR EN RUTAS PROTEGIDAS.
    """
    return _get_client_from_token_credentials(token, db)


def get_current_active_client_or_none(
    token: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    db: Session = Depends(get_db),
) -> Optional[client_model.Client]:
    """
    Dependencia que intenta obtener el cliente actual si se proporciona un token,
    pero devuelve None si el token no está, es inválido o el usuario no está activo.
    NO LANZA ERRORES. USAR PARA LÓGICA OPCIONAL.
    """
    if not token:
        return None
    try:
        return _get_client_from_token_credentials(token, db)
    except AuthenticationException:
        return None


def get_current_admin_user(
    current_client: client_model.Client = Depends(get_current_active_client),
) -> client_model.Client:
    """
    Dependencia que obtiene el cliente activo y verifica que sea administrador.
    """
    if not current_client.is_admin:
        raise AuthenticationException("Se requieren permisos de administrador.")
    return current_client