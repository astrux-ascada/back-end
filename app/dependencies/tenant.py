# /app/dependencies/tenant.py
"""
Dependencias de FastAPI relacionadas con la gestión del Tenant.
"""
import uuid
from fastapi import HTTPException, status

from app.core.context import tenant_id_context

def get_tenant_id() -> uuid.UUID:
    """
    Dependencia de FastAPI que obtiene el tenant_id del contexto de la petición.

    Esta dependencia asegura que el endpoint que la utiliza solo puede ser accedido
    en un contexto donde un tenant ha sido identificado por el TenantMiddleware.

    Lanza:
        HTTPException(400): Si no se encuentra un tenant_id en el contexto.

    Retorna:
        El UUID del tenant actual.
    """
    tenant_id = tenant_id_context.get()
    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo determinar el tenant para esta operación."
        )
    return tenant_id
