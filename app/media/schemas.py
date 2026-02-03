# /app/media/schemas.py
"""
Esquemas Pydantic para el Media Manager.
"""
import uuid
from pydantic import BaseModel, Field
from typing import Dict, Optional

from app.media.models import MediaItemStatus

# --- Esquemas para la API ---

class UploadRequest(BaseModel):
    context: str = Field(..., description="Contexto de negocio del archivo, ej: 'WORK_ORDER_EVIDENCE'.")
    context_id: Optional[uuid.UUID] = Field(None, description="ID de la entidad a la que se asocia el archivo.")
    original_filename: str = Field(..., description="Nombre original del archivo en el cliente.")
    content_type: str = Field(..., description="Tipo MIME del archivo, ej: 'image/jpeg'.")
    size_bytes: int = Field(..., description="Tamaño del archivo en bytes.")

class UploadRequestResponse(BaseModel):
    media_item_id: uuid.UUID
    upload_info: Dict[str, any]

class MediaItemRead(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    uploaded_by_id: uuid.UUID
    context: str
    context_id: Optional[uuid.UUID]
    original_filename: str
    content_type: str
    size_bytes: int
    status: MediaItemStatus
    download_url: Optional[str] = None # Se puede poblar en el servicio

    class Config:
        orm_mode = True
