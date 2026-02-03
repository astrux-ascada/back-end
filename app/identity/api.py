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
from app.dependencies.services import get_auth_service, get_audit_service
from app.dependencies.tenant import get_tenant_id
from app.identity.auth_service import AuthService
from app.auditing.service import AuditService
from app.identity.models import User
from app.identity.schemas import UserCreate, UserLogin, TokenWithUser, UserRead, TfaToken, UserUpdate

logger = logging.getLogger("app.identity.api")

router = APIRouter(prefix="/auth", tags=["Authentication"])


# --- Endpoints de Autenticación Principal ---

@router.post("/login", response_model=TokenWithUser)
@limiter.limit("10/minute")
def login_for_access_token(request: Request, form_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    """
    Autentica a un usuario y devuelve un token de acceso JWT.
    
    Verifica credenciales, estado de la suscripción del tenant y bloqueos de seguridad.
    """
    user = auth_service.login_user(email=form_data.email, password=form_data.password)
    access_token = auth_service.create_user_session(user)
    return TokenWithUser(access_token=access_token, user=user)

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Devuelve la información del usuario actualmente autenticado."""
    return current_user

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: Dict[str, Any] = Depends(get_current_token_payload), auth_service: AuthService = Depends(get_auth_service)):
    """Cierra la sesión actual invalidando el token en Redis."""
    jti = payload.get("jti")
    auth_service.logout_user(jti)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Endpoints de Gestión de Usuarios (Administración) ---

@router.get("/users", response_model=List[UserRead], dependencies=[Depends(get_current_admin_user)])
def list_users(
    skip: int = 0,
    limit: int = 100,
    auth_service: AuthService = Depends(get_auth_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """
    Obtiene una lista de todos los usuarios del tenant actual.
    Solo accesible para administradores.
    """
    return auth_service.list_users(tenant_id=tenant_id, skip=skip, limit=limit)

@router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: uuid.UUID, 
    user_in: UserUpdate, 
    auth_service: AuthService = Depends(get_auth_service),
    audit_service: AuditService = Depends(get_audit_service),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Actualiza la información de un usuario existente.
    Registra la operación en la auditoría.
    """
    updated_user = auth_service.update_user(user_id, user_in)
    
    audit_service.log_operation(
        user=current_user,
        action="UPDATE_USER",
        entity=updated_user,
        details=user_in.model_dump(exclude_unset=True)
    )
    return updated_user

@router.delete("/users/{user_id}", response_model=UserRead)
def delete_user(
    user_id: uuid.UUID, 
    auth_service: AuthService = Depends(get_auth_service),
    audit_service: AuditService = Depends(get_audit_service),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Desactiva (soft delete) a un usuario existente.
    Registra la operación en la auditoría.
    """
    deleted_user = auth_service.delete_user(user_id)
    
    audit_service.log_operation(
        user=current_user,
        action="DELETE_USER",
        entity=deleted_user
    )
    return deleted_user


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


# --- Endpoints de Administración ---

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenWithUser)
@limiter.limit("5/minute")
def register_user(
    request: Request, 
    user_data: UserCreate, 
    auth_service: AuthService = Depends(get_auth_service),
    audit_service: AuditService = Depends(get_audit_service),
    current_user: User = Depends(get_current_admin_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """
    Registra un nuevo usuario en el tenant actual.
    Solo accesible para administradores.
    """
    new_user = auth_service.register_user(user_data, tenant_id=tenant_id)
    
    audit_service.log_operation(
        user=current_user,
        action="REGISTER_USER",
        entity=new_user,
        details={"email": new_user.email, "role_ids": [str(r) for r in user_data.role_ids] if user_data.role_ids else []}
    )
    
    # Nota: Al registrar desde admin, no iniciamos sesión automáticamente para el nuevo usuario
    # Devolvemos un token vacío o cambiamos el modelo de respuesta, pero para mantener compatibilidad:
    access_token = "" 
    return TokenWithUser(access_token=access_token, user=new_user)

@router.post("/sessions/clear-all", dependencies=[Depends(get_current_admin_user)])
def clear_all_sessions(
    auth_service: AuthService = Depends(get_auth_service),
    audit_service: AuditService = Depends(get_audit_service),
    current_user: User = Depends(get_current_admin_user),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """
    Invalida todas las sesiones activas (logout forzado).
    TODO: Implementar filtrado por tenant_id en el servicio.
    """
    invalidated_count = auth_service.logout_all_users(tenant_id=tenant_id)
    
    audit_service.log_operation(
        user=current_user,
        action="CLEAR_ALL_SESSIONS",
        entity=current_user, # Entidad simbólica
        details={"count": invalidated_count}
    )
    return {"message": f"Todas las sesiones de usuario activas han sido invalidadas.", "invalidated_sessions": invalidated_count}
