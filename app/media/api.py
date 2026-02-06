# /app/media/api.py
"""
API Router para el Media Manager.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict

from app.media.service import MediaService
from app.dependencies.services import get_media_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.auth import get_current_active_user
from app.identity.models import User
from app.media import schemas
from app.core.exceptions import NotFoundException, PermissionDeniedException # Importar excepciones

router = APIRouter(prefix="/media", tags=["Media"])

@router.post(
    "/upload-request",
    summary="Solicitar una URL para subir un archivo",
    response_model=schemas.UploadRequestResponse,
)
def request_upload_url(
    request_in: schemas.UploadRequest,
    media_service: MediaService = Depends(get_media_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user),
):
    """
    Inicia el proceso de subida de un archivo.
    
    El cliente proporciona el contexto y los metadatos del archivo, y el backend
    devuelve una URL presignada donde el cliente debe subir el archivo directamente.
    """
    upload_data = media_service.request_upload_url(
        tenant_id=tenant_id,
        user_id=current_user.id,
        context=request_in.context,
        context_id=request_in.context_id,
        original_filename=request_in.original_filename,
        content_type=request_in.content_type,
        size_bytes=request_in.size_bytes
    )
    return upload_data


@router.post(
    "/{media_item_id}/confirm-upload",
    summary="Confirmar que un archivo ha sido subido",
    response_model=schemas.MediaItemRead,
)
def confirm_upload(
    media_item_id: uuid.UUID,
    media_service: MediaService = Depends(get_media_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user),
):
    """
    Confirma al backend que el archivo fue subido exitosamente a la URL presignada.
    
    El backend actualiza el estado del MediaItem a 'AVAILABLE'.
    """
    try:
        media_item = media_service.confirm_upload(
            media_item_id=media_item_id,
            tenant_id=tenant_id,
            user_id=current_user.id
        )
        return media_item
    except (NotFoundException, PermissionDeniedException) as e:
        # Es mejor devolver 403 para PermissionDenied y 404 para NotFound
        if isinstance(e, PermissionDeniedException):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
