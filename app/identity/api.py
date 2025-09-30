# /app/identity/api.py
"""
API Router para la autenticación de usuarios de Astruxa.

Define los endpoints para el registro y el inicio de sesión, siguiendo
los estándares de la arquitectura modular y limpia.
"""

import logging

from fastapi import APIRouter, Depends, Request, status

from app.core.limiter import limiter
from app.dependencies.services import get_auth_service
from app.identity.auth_service import AuthService
from app.identity.schemas import UserCreate, UserLogin, TokenWithUser

logger = logging.getLogger("app.identity.api")

router = APIRouter(tags=["Authentication"])


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
    """
    Registra un nuevo usuario, crea una sesión en Redis y devuelve un token de acceso.
    """
    new_user = auth_service.register_user(user_data)
    # --- MEJORA: Llamar al servicio para crear la sesión y obtener el token ---
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
    """
    Autentica a un usuario, crea una sesión en Redis y devuelve un token de acceso JWT.
    """
    user = auth_service.login_user(email=form_data.email, password=form_data.password)
    # --- MEJORA: Llamar al servicio para crear la sesión y obtener el token ---
    access_token = auth_service.create_user_session(user)
    logger.info(f"Inicio de sesión y sesión creada para: {user.email}")
    return TokenWithUser(access_token=access_token, user=user)
