# /app/auditing/models/audit_log.py
"""
Modelo de la base de datos para la entidad AuditLog.

Registra eventos de negocio y operaciones importantes para la trazabilidad.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.base_class import Base


class AuditLog(Base):
    """Modelo SQLAlchemy para un Registro de Auditoría."""
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    
    # Quién realizó la acción (puede ser nulo si es una acción del sistema)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    
    # Qué se modificó
    entity_type = Column(String(50), nullable=False, index=True) # Ej: "WorkOrder", "Asset"
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # La acción realizada
    action = Column(String(100), nullable=False, index=True) # Ej: "UPDATE_STATUS", "CREATE_ASSET"
    
    # Detalles del cambio (antes y después)
    details = Column(JSONB, nullable=True, comment="JSON data detailing the change, e.g., {'from': 'old_value', 'to': 'new_value'}.")
