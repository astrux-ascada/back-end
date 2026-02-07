# /app/media/api.py
"""
API Router para el Media Manager.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Dict

from app.media.service import MediaService
from app.dependencies.services import get_media_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.auth import get_current_active_user
from app.identity.models import User
from app.media import schemas
from app.core.exceptions import NotFoundException, PermissionDeniedException

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
    devuelve una URL presignada (o una ruta de API para subida local) donde el 
    cliente debe subir el archivo.
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

@router.put(
    "/local-upload/{file_path:path}",
    summary="Subir un archivo al almacenamiento local (para desarrollo)",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def upload_local_file(
    file_path: str,
    file: UploadFile = File(...),
    media_service: MediaService = Depends(get_media_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user),
):
    """
    Endpoint para manejar la subida de archivos cuando se usa la estrategia 'local'.
    El frontend usa este endpoint como si fuera una URL presignada.
    """
    # Aquí podríamos añadir validaciones de seguridad:
    # - ¿El file_path realmente pertenece al tenant_id?
    # - ¿El usuario actual tiene permiso para escribir en esta ruta?
    # Por ahora, confiamos en que la ruta generada es segura.
    
    success = media_service.storage.save_file(file_path, file.file)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo guardar el archivo.")
    
    return


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
    Confirma al backend que el archivo fue subido exitosamente.
    
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
        if isinstance(e, PermissionDeniedException):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
