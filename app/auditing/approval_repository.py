# /app/auditing/approval_repository.py
"""
Capa de Repositorio para el módulo de Aprobaciones.
"""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.auditing.models.approval_request import ApprovalRequest, ApprovalStatus
from app.auditing import schemas # Asumo que crearemos schemas para esto

class ApprovalRepository:
    """Realiza operaciones CRUD para las solicitudes de aprobación."""

    def __init__(self, db: Session):
        self.db = db

    def create_request(self, request_in: schemas.ApprovalRequestCreate, tenant_id: uuid.UUID, requester_id: uuid.UUID) -> ApprovalRequest:
        db_request = ApprovalRequest(
            **request_in.model_dump(),
            tenant_id=tenant_id,
            requester_id=requester_id,
            status=ApprovalStatus.PENDING
        )
        self.db.add(db_request)
        self.db.commit()
        self.db.refresh(db_request)
        return db_request

    def get_request(self, request_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[ApprovalRequest]:
        return self.db.query(ApprovalRequest).filter(
            ApprovalRequest.id == request_id,
            ApprovalRequest.tenant_id == tenant_id
        ).first()

    def list_pending_requests(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[ApprovalRequest]:
        return self.db.query(ApprovalRequest).filter(
            ApprovalRequest.tenant_id == tenant_id,
            ApprovalRequest.status == ApprovalStatus.PENDING
        ).offset(skip).limit(limit).all()

    def update_status(self, request: ApprovalRequest, status: ApprovalStatus, approver_id: uuid.UUID, rejection_reason: Optional[str] = None) -> ApprovalRequest:
        request.status = status
        request.approver_id = approver_id
        if rejection_reason:
            request.rejection_reason = rejection_reason
        
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request
