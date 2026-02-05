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
from app.dependencies.services import get_audit_service, get_approval_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.permissions import require_permission
from app.identity.models import User
from app.dependencies.auth import get_current_active_user

logger = logging.getLogger("app.auditing.api")

router = APIRouter(prefix="/auditing", tags=["Auditing & Approvals"])

# --- Endpoints para AuditLog ---

@router.get("/logs", response_model=List[schemas.AuditLogRead], dependencies=[Depends(require_permission("audit_log:read"))])
def list_audit_logs(
    skip: int = 0,
    limit: int = 100,
    audit_service: AuditService = Depends(get_audit_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return audit_service.list_logs(tenant_id, skip, limit)

# --- Endpoints para ApprovalRequest ---

@router.get("/approvals/pending", response_model=List[schemas.ApprovalRequestRead], dependencies=[Depends(require_permission("approval:read"))])
def list_pending_approvals(
    approval_service: ApprovalService = Depends(get_approval_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
):
    return approval_service.list_pending_requests(tenant_id)

@router.post("/approvals/{request_id}/decide", response_model=schemas.ApprovalRequestRead, dependencies=[Depends(require_permission("approval:decide"))])
def decide_on_request(
    request_id: uuid.UUID,
    decision: schemas.ApprovalDecision,
    approval_service: ApprovalService = Depends(get_approval_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    try:
        return approval_service.process_decision(request_id, decision, current_user, tenant_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
