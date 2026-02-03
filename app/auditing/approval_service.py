# /app/auditing/approval_service.py
"""
Capa de Servicio para el módulo de Aprobaciones.
"""
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.auditing import models, schemas
from app.auditing.approval_repository import ApprovalRepository
from app.auditing.models.approval_request import ApprovalStatus
from app.core.exceptions import NotFoundException, PermissionDeniedException
from app.identity.models import User

class ApprovalService:
    """Servicio de negocio para la gestión de aprobaciones (Maker-Checker)."""

    def __init__(self, db: Session):
        self.db = db
        self.approval_repo = ApprovalRepository(self.db)

    def create_request(
        self, 
        request_in: schemas.ApprovalRequestCreate, 
        requester: User, 
        tenant_id: uuid.UUID
    ) -> schemas.ApprovalRequestRead:
        """Crea una nueva solicitud de aprobación."""
        # Aquí se podría notificar a los aprobadores (ej: via email/notificación interna)
        request = self.approval_repo.create_request(request_in, tenant_id, requester.id)
        return request

    def list_pending_requests(self, tenant_id: uuid.UUID) -> List[schemas.ApprovalRequestRead]:
        """Lista las solicitudes pendientes para el tenant."""
        return self.approval_repo.list_pending_requests(tenant_id)

    def process_decision(
        self, 
        request_id: uuid.UUID, 
        decision: schemas.ApprovalDecision, 
        approver: User, 
        tenant_id: uuid.UUID
    ) -> models.ApprovalRequest:
        """
        Procesa la decisión de un aprobador.
        
        Retorna la solicitud actualizada.
        Si el estado es APPROVED, el llamador (API) debe ejecutar la acción correspondiente.
        """
        request = self.approval_repo.get_request(request_id, tenant_id)
        if not request:
            raise NotFoundException("Approval request not found.")
        
        if request.status != ApprovalStatus.PENDING:
            raise PermissionDeniedException("This request has already been processed.")

        # Validar que el aprobador no sea el mismo solicitante (Principio de 4 ojos)
        if request.requester_id == approver.id:
            raise PermissionDeniedException("You cannot approve your own request.")

        new_status = ApprovalStatus.APPROVED if decision.approved else ApprovalStatus.REJECTED
        
        if new_status == ApprovalStatus.REJECTED and not decision.rejection_reason:
            raise ValueError("Rejection reason is required when rejecting a request.")

        updated_request = self.approval_repo.update_status(
            request, 
            new_status, 
            approver.id, 
            decision.rejection_reason
        )
        
        return updated_request
