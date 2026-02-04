# /app/auditing/approval_service.py
"""
Capa de Servicio para el módulo de Aprobaciones.
"""
import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session

from app.auditing import models, schemas
from app.auditing.approval_repository import ApprovalRepository
from app.auditing.models.approval_request import ApprovalStatus
from app.core.exceptions import NotFoundException, PermissionDeniedException
from app.identity.models import User

if TYPE_CHECKING:
    from app.assets.service import AssetService

class ApprovalService:
    """Servicio de negocio para la gestión de aprobaciones (Maker-Checker)."""

    def __init__(self, db: Session, asset_service: Optional['AssetService'] = None):
        self.db = db
        self.asset_service = asset_service
        self.approval_repo = ApprovalRepository(self.db)

    def create_request(self, request_in: schemas.ApprovalRequestCreate, requester: User, tenant_id: uuid.UUID) -> schemas.ApprovalRequestRead:
        request = self.approval_repo.create_request(request_in, tenant_id, requester.id)
        return request

    def list_pending_requests(self, tenant_id: uuid.UUID) -> List[schemas.ApprovalRequestRead]:
        return self.approval_repo.list_pending_requests(tenant_id)

    def process_decision(self, request_id: uuid.UUID, decision: schemas.ApprovalDecision, approver: User, tenant_id: uuid.UUID) -> models.ApprovalRequest:
        request = self.approval_repo.get_request(request_id, tenant_id)
        if not request:
            raise NotFoundException("Approval request not found.")
        
        if request.status != ApprovalStatus.PENDING:
            raise PermissionDeniedException("This request has already been processed.")

        if request.requester_id == approver.id:
            raise PermissionDeniedException("You cannot approve your own request.")

        new_status = ApprovalStatus.APPROVED if decision.approved else ApprovalStatus.REJECTED
        
        if new_status == ApprovalStatus.REJECTED and not decision.rejection_reason:
            raise ValueError("Rejection reason is required when rejecting a request.")

        if new_status == ApprovalStatus.APPROVED:
            self._execute_approved_action(request)

        updated_request = self.approval_repo.update_status(request, new_status, approver.id, decision.rejection_reason)
        return updated_request

    def _execute_approved_action(self, request: models.ApprovalRequest):
        """
        (Método interno) Llama al servicio correspondiente para ejecutar la acción aprobada.
        """
        # Importación diferida para romper el ciclo
        from app.assets.service import AssetService

        if request.action == "DELETE_ASSET":
            if not self.asset_service:
                raise RuntimeError("AssetService no está disponible para ejecutar la acción.")
            
            # Aquí ya podemos usar AssetService porque lo importamos localmente
            if isinstance(self.asset_service, AssetService):
                self.asset_service._execute_delete_asset(request.entity_id, request.tenant_id)
            else:
                # Fallback por si la inyección falló de alguna manera extraña
                raise RuntimeError("El servicio inyectado no es una instancia válida.")
        else:
            pass
