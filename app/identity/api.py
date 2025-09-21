# /app/identity/api.py
"""
API Router para la autenticación de usuarios de Astruxa.

Define los endpoints para el registro y el inicio de sesión, siguiendo
los estándares de la arquitectura modular y limpia.
"""

import logging

from fastapi import APIRouter, Depends, Request, status

from app.core.limiter import limiter
from app.core.security import create_access_token
from app.dependencies.services import get_auth_service
from app.identity.auth_service import AuthService
from app.identity.schemas import UserCreate, UserLogin, TokenWithUser

logger = logging.getLogger("app.identity.api")

router = APIRouter(tags=["Authentication"])


@router.post(
    "/register",
    summary="Registrar un nuevo usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenWithUser,
)
@limiter.limit("5/minute")
def register_user(
    request: Request,  # Necesario para el rate limiter
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Registra un nuevo usuario y devuelve un token de acceso junto con los datos del usuario.
    """
    new_user = auth_service.register_user(user_data)
    access_token = create_access_token(new_user)
    logger.info(f"Nuevo usuario registrado: {new_user.email}")
    return TokenWithUser(access_token=access_token, user=new_user)


@router.post(
    "/login",
    summary="Iniciar sesión y obtener un token JWT",
    response_model=TokenWithUser,
)
@limiter.limit("10/minute")
def login_for_access_token(
    request: Request,  # Necesario para el rate limiter
    form_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Autentica a un usuario y devuelve un token de acceso JWT.
    """
    user = auth_service.login_user(email=form_data.email, password=form_data.password)
    access_token = create_access_token(user)
    logger.info(f"Inicio de sesión exitoso para: {user.email}")
    return TokenWithUser(access_token=access_token, user=user)
