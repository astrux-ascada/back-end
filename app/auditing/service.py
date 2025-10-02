# /app/auditing/service.py
"""
Capa de Servicio para el módulo de Auditoría.
"""

from typing import List, Optional, Any, Dict
import uuid
from sqlalchemy.orm import Session

from app.auditing import models, schemas
from app.auditing.repository import AuditLogRepository
from app.identity.models import User # Necesario para tipar el usuario que realiza la acción


class AuditService:
    """Servicio de negocio para la gestión de logs de auditoría."""

    def __init__(self, db: Session):
        self.db = db
        self.audit_repo = AuditLogRepository(self.db)

    def log_operation(
        self, 
        user: Optional[User],
        action: str, 
        entity: Any, 
        details: Optional[Dict[str, Any]] = None
    ) -> models.AuditLog:
        """
        Registra una operación de negocio en el log de auditoría.

        Args:
            user: El usuario que realiza la acción (si aplica).
            action: La acción realizada (ej: "UPDATE_STATUS").
            entity: El objeto de SQLAlchemy que fue modificado.
            details: Un diccionario con los detalles del cambio.
        """
        log_entry = schemas.AuditLogCreate(
            user_id=user.id if user else None,
            entity_type=entity.__class__.__name__,
            entity_id=entity.id,
            action=action,
            details=details
        )
        return self.audit_repo.create_log(log_entry)

    def list_logs(self, skip: int = 0, limit: int = 100) -> List[models.AuditLog]:
        """Lista los registros de auditoría."""
        return self.audit_repo.list_logs(skip, limit)
