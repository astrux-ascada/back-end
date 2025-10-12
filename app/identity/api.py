# /app/identity/api.py
"""
API Router para la autenticación y gestión de usuarios de Astruxa.
"""

import logging
import uuid
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, Request, status, Response, HTTPException

from app.core.limiter import limiter
from app.dependencies.auth import get_current_token_payload, get_current_admin_user, get_current_active_user
from app.dependencies.services import get_auth_service
from app.identity.auth_service import AuthService
from app.identity.models import User
from app.identity.schemas import UserCreate, UserLogin, TokenWithUser, UserRead, TfaToken, UserUpdate

logger = logging.getLogger("app.identity.api")

router = APIRouter(prefix="/auth", tags=["Authentication"])


# --- Endpoints de Autenticación Principal ---

@router.post("/login", response_model=TokenWithUser)
@limiter.limit("10/minute")
def login_for_access_token(request: Request, form_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    user = auth_service.login_user(email=form_data.email, password=form_data.password)
    access_token = auth_service.create_user_session(user)
    return TokenWithUser(access_token=access_token, user=user)

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: Dict[str, Any] = Depends(get_current_token_payload), auth_service: AuthService = Depends(get_auth_service)):
    jti = payload.get("jti")
    auth_service.logout_user(jti)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Endpoints de Gestión de Usuarios (Administración) ---

@router.get("/users", response_model=List[UserRead], dependencies=[Depends(get_current_admin_user)])
def list_users(
    skip: int = 0,
    limit: int = 100,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Obtiene una lista de todos los usuarios del sistema."""
    return auth_service.list_users(skip=skip, limit=limit)

@router.put("/users/{user_id}", response_model=UserRead, dependencies=[Depends(get_current_admin_user)])
def update_user(user_id: uuid.UUID, user_in: UserUpdate, auth_service: AuthService = Depends(get_auth_service)):
    """Actualiza la información de un usuario existente."""
    return auth_service.update_user(user_id, user_in)

@router.delete("/users/{user_id}", response_model=UserRead, dependencies=[Depends(get_current_admin_user)])
def delete_user(user_id: uuid.UUID, auth_service: AuthService = Depends(get_auth_service)):
    """Desactiva (soft delete) a un usuario existente."""
    return auth_service.delete_user(user_id)


# --- Endpoints de Gestión de 2FA ---

@router.post("/tfa/setup", response_model=Dict[str, str])
def setup_tfa(current_user: User = Depends(get_current_active_user), auth_service: AuthService = Depends(get_auth_service)):
    """Genera un nuevo secreto 2FA para el usuario y devuelve la URL para el código QR."""
    return auth_service.setup_tfa(current_user)

@router.post("/tfa/enable", status_code=status.HTTP_204_NO_CONTENT)
def enable_tfa(token_data: TfaToken, current_user: User = Depends(get_current_active_user), auth_service: AuthService = Depends(get_auth_service)):
    """Verifica el token inicial y activa el 2FA para la cuenta del usuario."""
    if not auth_service.enable_tfa(current_user, token_data.token):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token 2FA inválido.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/verify-token", response_model=Dict[str, bool])
def verify_tfa_token(token_data: TfaToken, current_user: User = Depends(get_current_active_user), auth_service: AuthService = Depends(get_auth_service)):
    """Verifica un token 2FA para una operación crítica."""
    if not auth_service.verify_tfa_token(current_user, token_data.token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 2FA inválido o incorrecto.")
    return {"verified": True}


# --- Endpoints de Administración (pueden moverse a un router /admin en el futuro) ---

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenWithUser, dependencies=[Depends(get_current_admin_user)])
@limiter.limit("5/minute")
def register_user(request: Request, user_data: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    new_user = auth_service.register_user(user_data)
    access_token = auth_service.create_user_session(new_user)
    return TokenWithUser(access_token=access_token, user=new_user)

@router.post("/sessions/clear-all", dependencies=[Depends(get_current_admin_user)])
def clear_all_sessions(auth_service: AuthService = Depends(get_auth_service)):
    invalidated_count = auth_service.logout_all_users()
    return {"message": f"Todas las sesiones de usuario activas han sido invalidadas.", "invalidated_sessions": invalidated_count}
