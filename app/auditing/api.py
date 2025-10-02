# /app/auditing/api.py
"""
API Router para el módulo de Auditoría.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends

from app.auditing import schemas
from app.auditing.service import AuditService
from app.dependencies.auth import get_current_admin_user
from app.dependencies.services import get_audit_service

logger = logging.getLogger("app.auditing.api")

router = APIRouter(prefix="/auditing", tags=["Auditing"])


@router.get(
    "/logs",
    summary="[Admin] Obtener el historial de operaciones",
    response_model=List[schemas.AuditLogRead],
    dependencies=[Depends(get_current_admin_user)],
)
def list_audit_logs(
    skip: int = 0,
    limit: int = 100,
    audit_service: AuditService = Depends(get_audit_service),
):
    """Devuelve una lista paginada de todos los registros de auditoría del sistema."""
    return audit_service.list_logs(skip=skip, limit=limit)
