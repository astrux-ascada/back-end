# /app/identity/api.py
"""
API Router para la autenticación de usuarios de Astruxa.

Define los endpoints para el registro, el inicio de sesión y el cierre de sesión.
"""

import logging
from typing import Dict, Any

from fastapi import APIRouter, Depends, Request, status, Response

from app.core.limiter import limiter
# --- MEJORA: Importar las dependencias de autorización ---
from app.dependencies.auth import get_current_token_payload, get_current_admin_user, get_current_active_user
from app.dependencies.services import get_auth_service
from app.identity.auth_service import AuthService
from app.identity.models import User
from app.identity.schemas import UserCreate, UserLogin, TokenWithUser, UserRead

logger = logging.getLogger("app.identity.api")

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    summary="Registrar un nuevo usuario y crear una sesión",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenWithUser,
)
@limiter.limit("5/minute")
def register_user(
    request: Request,
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    new_user = auth_service.register_user(user_data)
    access_token = auth_service.create_user_session(new_user)
    logger.info(f"Nuevo usuario registrado y sesión creada para: {new_user.email}")
    return TokenWithUser(access_token=access_token, user=new_user)


@router.post(
    "/login",
    summary="Iniciar sesión y obtener un token JWT",
    response_model=TokenWithUser,
)
@limiter.limit("10/minute")
def login_for_access_token(
    request: Request,
    form_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.login_user(email=form_data.email, password=form_data.password)
    access_token = auth_service.create_user_session(user)
    logger.info(f"Inicio de sesión y sesión creada para: {user.email}")
    return TokenWithUser(access_token=access_token, user=user)


@router.get(
    "/me",
    summary="Obtener los datos del usuario actual",
    response_model=UserRead,
)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Devuelve el objeto completo del usuario autenticado actualmente.
    """
    return current_user


@router.post(
    "/logout",
    summary="Cerrar sesión e invalidar el token actual",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    payload: Dict[str, Any] = Depends(get_current_token_payload),
    auth_service: AuthService = Depends(get_auth_service),
):
    jti = payload.get("jti")
    auth_service.logout_user(jti)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Endpoint del Recolector de Sesiones ---
@router.post(
    "/sessions/clear-all",
    summary="[Admin] Invalidar todas las sesiones de usuario activas",
    dependencies=[Depends(get_current_admin_user)],
)
def clear_all_sessions(auth_service: AuthService = Depends(get_auth_service)):
    """
    Invalida TODAS las sesiones de usuario activas eliminándolas de Redis.
    """
    invalidated_count = auth_service.logout_all_users()
    return {
        "message": f"Todas las sesiones de usuario activas han sido invalidadas.",
        "invalidated_sessions": invalidated_count,
    }
