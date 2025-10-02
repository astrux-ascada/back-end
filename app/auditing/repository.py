# /app/auditing/repository.py
"""
Capa de Repositorio para el módulo de Auditoría.
"""

from typing import List
from sqlalchemy.orm import Session

from app.auditing import models, schemas


class AuditLogRepository:
    """Realiza operaciones de escritura y lectura en la base de datos para los logs de auditoría."""

    def __init__(self, db: Session):
        self.db = db

    def create_log(self, log_in: schemas.AuditLogCreate) -> models.AuditLog:
        """Crea un nuevo registro de auditoría en la base de datos."""
        db_log = models.AuditLog(**log_in.model_dump())
        self.db.add(db_log)
        self.db.commit()
        self.db.refresh(db_log)
        return db_log

    def list_logs(self, skip: int = 0, limit: int = 100) -> List[models.AuditLog]:
        """Lista todos los registros de auditoría con paginación."""
        return self.db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
