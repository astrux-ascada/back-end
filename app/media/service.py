# /app/media/service.py
"""
Capa de Servicio para el Media Manager.
"""
import uuid
from sqlalchemy.orm import Session
from typing import Dict, Optional

from app.media.storage import get_storage_strategy, StorageInterface
from app.media.models import MediaItem, MediaItemStatus
from app.core.exceptions import NotFoundException, PermissionDeniedException

class MediaService:
    """Servicio de negocio para la gestión de archivos multimedia."""

    def __init__(self, db: Session):
        self.db = db
        self.storage: StorageInterface = get_storage_strategy()

    def request_upload_url(
        self,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
        context: str,
        context_id: Optional[uuid.UUID],
        original_filename: str,
        content_type: str,
        size_bytes: int
    ) -> Dict[str, any]:
        """
        1. Genera una ruta segura para el archivo.
        2. Crea un registro MediaItem en la BD.
        3. Devuelve una URL presignada para que el cliente suba el archivo.
        """
        # Generar un nombre de archivo único y la ruta estructurada
        file_extension = original_filename.split('.')[-1] if '.' in original_filename else ''
        file_uuid = uuid.uuid4()
        file_path = f"tenants/{tenant_id}/{context.lower()}/{context_id or 'global'}/{file_uuid}.{file_extension}"

        # Crear el registro en la base de datos
        db_media_item = MediaItem(
            id=file_uuid,
            tenant_id=tenant_id,
            uploaded_by_id=user_id,
            context=context,
            context_id=context_id,
            file_path=file_path,
            original_filename=original_filename,
            content_type=content_type,
            size_bytes=size_bytes,
            status=MediaItemStatus.PENDING_UPLOAD
        )
        self.db.add(db_media_item)
        self.db.commit()
        self.db.refresh(db_media_item)

        # Obtener la URL presignada del servicio de almacenamiento
        upload_info = self.storage.generate_upload_url(file_path, content_type)

        return {
            "media_item_id": db_media_item.id,
            "upload_info": upload_info
        }

    def confirm_upload(
        self,
        media_item_id: uuid.UUID,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> MediaItem:
        """
        Confirma que un archivo ha sido subido y actualiza su estado a 'AVAILABLE'.
        """
        db_media_item = self.db.query(MediaItem).filter(
            MediaItem.id == media_item_id,
            MediaItem.tenant_id == tenant_id
        ).first()

        if not db_media_item:
            raise NotFoundException("Media item not found.")
        
        # Opcional: Verificar que el usuario que confirma es el que inició la subida
        if db_media_item.uploaded_by_id != user_id:
            raise PermissionDeniedException("You do not have permission to confirm this upload.")

        # Opcional: Verificar en el backend de almacenamiento si el archivo existe.
        # if not self.storage.file_exists(db_media_item.file_path):
        #     db_media_item.status = MediaItemStatus.ERROR
        #     self.db.commit()
        #     raise NotFoundException("File not found in storage backend after upload.")

        db_media_item.status = MediaItemStatus.AVAILABLE
        self.db.commit()
        self.db.refresh(db_media_item)

        return db_media_item
