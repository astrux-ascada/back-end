# /app/auditing/api.py
"""
API Router para el módulo de Auditoría y Aprobaciones.
"""

import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from app.auditing import schemas
from app.auditing.service import AuditService
from app.auditing.approval_service import ApprovalService
from app.dependencies.auth import get_current_admin_user, get_current_active_user
from app.dependencies.services import get_audit_service, get_approval_service
from app.dependencies.tenant import get_tenant_id
from app.identity.models import User

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

# --- Endpoints de Aprobaciones ---

@router.get(
    "/approvals/pending",
    summary="Listar solicitudes de aprobación pendientes",
    response_model=List[schemas.ApprovalRequestRead],
)
def list_pending_approvals(
    approval_service: ApprovalService = Depends(get_approval_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user), # Debería ser un rol con permisos de aprobación
):
    """Lista las solicitudes que requieren aprobación."""
    return approval_service.list_pending_requests(tenant_id)

@router.post(
    "/approvals/{request_id}/decide",
    summary="Aprobar o rechazar una solicitud",
    response_model=schemas.ApprovalRequestRead,
)
def decide_approval(
    request_id: uuid.UUID,
    decision: schemas.ApprovalDecision,
    approval_service: ApprovalService = Depends(get_approval_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user),
):
    """Procesa la decisión de un aprobador."""
    try:
        return approval_service.process_decision(request_id, decision, current_user, tenant_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Capturar excepciones de permisos o not found
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
