# /app/dependencies/tenant.py
"""
Dependencias de FastAPI relacionadas con la gestión del Tenant.
"""
import uuid
from typing import Dict, Any
from fastapi import HTTPException, status, Depends

from app.core.context import tenant_id_context
from app.dependencies.auth import get_current_token_payload

def get_tenant_id(payload: Dict[str, Any] = Depends(get_current_token_payload)) -> uuid.UUID:
    """
    Dependencia de FastAPI que obtiene el tenant_id del payload del token JWT.

    Esta dependencia asegura que el endpoint que la utiliza solo puede ser accedido
    por un usuario con un token válido que contenga un tenant_id.

    Lanza:
        HTTPException(400): Si no se encuentra un tenant_id en el token.

    Retorna:
        El UUID del tenant actual.
    """
    tenant_id_str = payload.get("tenant_id")
    
    if tenant_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo determinar el tenant para esta operación (token inválido)."
        )
        
    try:
        tenant_id = uuid.UUID(tenant_id_str)
        # Establecer el tenant_id en el contexto para que otros servicios puedan usarlo
        tenant_id_context.set(tenant_id)
        return tenant_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El tenant_id en el token no es un UUID válido."
        )
