"""
Módulo para dependencias de autorización.

Estas funciones validan si un usuario autenticado tiene los permisos necesarios
para realizar una acción específica sobre un recurso.
"""

import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_db
from app.dependencies.auth import get_current_active_client
from app.models import client as client_model


async def get_authorized_client_for_contact_view(
        client_uuid: uuid.UUID,
        current_client: client_model.Client = Depends(get_current_active_client),
        db: Session = Depends(get_db),
) -> client_model.Client:
    """
    Dependencia que valida si el usuario actual puede ver los contactos de un cliente.

    - Un admin puede ver los contactos de cualquier cliente.
    - Un usuario normal solo puede ver sus propios contactos.

    Devuelve el objeto del cliente objetivo si está autorizado, si no, lanza una excepción.
    """
    if current_client.is_admin:
        target_client = (
            db.query(client_model.Client).filter(client_model.Client.uuid == client_uuid).first()
        )
        if not target_client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con UUID {client_uuid} no encontrado.",
            )
        return target_client

    if current_client.uuid != client_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver los contactos de este cliente.",
        )

    return current_client
