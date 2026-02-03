# /app/media/models.py
"""
Modelo de Base de Datos para el Media Manager.
"""
import uuid
import enum
from sqlalchemy import Column, String, ForeignKey, DateTime, func, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class MediaItemStatus(str, enum.Enum):
    PENDING_UPLOAD = "PENDING_UPLOAD"  # Se ha solicitado URL, pero el archivo no ha sido confirmado.
    AVAILABLE = "AVAILABLE"            # El archivo ha sido subido y confirmado.
    ERROR = "ERROR"                    # Hubo un error durante la subida o confirmación.
    DELETED = "DELETED"                # Marcado para borrado (soft delete).

class MediaItem(Base):
    __tablename__ = "media_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # --- Aislamiento y Propiedad ---
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    uploaded_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # --- Contexto de Negocio ---
    # A qué entidad pertenece este archivo (ej: 'WORK_ORDER', 'USER_AVATAR')
    context = Column(String(100), nullable=False, index=True)
    # El UUID de la entidad específica (ej: el id de la orden de trabajo)
    context_id = Column(UUID(as_uuid=True), nullable=True, index=True)

    # --- Metadata del Archivo ---
    # Ruta generada por el backend donde se almacena el archivo.
    file_path = Column(String(1024), nullable=False, unique=True)
    # Nombre original del archivo en el cliente.
    original_filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    
    # --- Ciclo de Vida ---
    status = Column(String, default=MediaItemStatus.PENDING_UPLOAD, nullable=False)

    # --- Auditoría ---
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
