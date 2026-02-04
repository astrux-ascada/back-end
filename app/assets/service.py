# /app/assets/service.py
"""
Capa de Servicio para el módulo de Activos (Assets).
"""

from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.assets import models, schemas
from app.assets.repository import AssetRepository
from app.assets.mappers import map_asset_to_dto
from app.auditing.service import AuditService
from app.auditing.approval_service import ApprovalService
from app.auditing.schemas import ApprovalRequestRead # Importar el esquema correcto
from app.identity.models import User
from app.core.exceptions import NotFoundException, ConflictException

class AssetService:
    """Servicio de negocio para la gestión de activos."""

    def __init__(self, db: Session, audit_service: AuditService, approval_service: ApprovalService):
        self.db = db
        self.audit_service = audit_service
        self.approval_service = approval_service
        self.asset_repo = AssetRepository(self.db)

    def create_asset(self, asset_in: schemas.AssetCreate, user: User, tenant_id: uuid.UUID) -> schemas.AssetReadDTO:
        db_asset = self.asset_repo.create_asset(asset_in, tenant_id)
        self.audit_service.log_operation(user=user, action="CREATE_ASSET", entity=db_asset)
        return map_asset_to_dto(db_asset, self.asset_repo)

    def get_asset(self, asset_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[schemas.AssetReadDTO]:
        asset = self.asset_repo.get_asset(asset_id, tenant_id)
        if asset:
            return map_asset_to_dto(asset, self.asset_repo)
        return None

    def list_assets(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100, category: Optional[str] = None, sector_id: Optional[uuid.UUID] = None) -> List[schemas.AssetReadDTO]:
        assets = self.asset_repo.list_assets(tenant_id, skip, limit, category, sector_id)
        return [map_asset_to_dto(asset, self.asset_repo) for asset in assets]

    def update_asset(self, asset_id: uuid.UUID, asset_in: schemas.AssetUpdate, user: User, tenant_id: uuid.UUID) -> Optional[schemas.AssetReadDTO]:
        db_asset = self.asset_repo.get_asset(asset_id, tenant_id)
        if not db_asset:
            return None
        updated_asset = self.asset_repo.update_asset(db_asset=db_asset, asset_in=asset_in)
        self.audit_service.log_operation(user=user, action="UPDATE_ASSET", entity=updated_asset, details=asset_in.model_dump(exclude_unset=True))
        return map_asset_to_dto(updated_asset, self.asset_repo)

    def update_asset_status(self, asset_id: uuid.UUID, status_update: schemas.AssetStatusUpdate, user: User, tenant_id: uuid.UUID) -> Optional[schemas.AssetReadDTO]:
        asset_before_update = self.asset_repo.get_asset(asset_id, tenant_id)
        if not asset_before_update:
            return None
        old_status = asset_before_update.status
        new_status = status_update.status
        updated_asset = self.asset_repo.update_asset_status(asset_id, tenant_id, new_status)
        if updated_asset:
            self.audit_service.log_operation(user=user, action="UPDATE_STATUS", entity=updated_asset, details={"from": old_status, "to": new_status})
            return map_asset_to_dto(updated_asset, self.asset_repo)
        return None

    def request_delete_asset(self, asset_id: uuid.UUID, user: User, tenant_id: uuid.UUID, justification: str) -> ApprovalRequestRead:
        """
        Inicia el proceso de borrado de un activo, creando una solicitud de aprobación.
        """
        db_asset = self.asset_repo.get_asset(asset_id, tenant_id)
        if not db_asset:
            raise NotFoundException("Activo no encontrado.")
        if db_asset.status != "operational":
            raise ConflictException(f"El activo no está en estado 'operational', no se puede solicitar su borrado.")

        # Cambiar estado a pendiente de borrado
        db_asset.status = "pending_deletion"
        self.db.commit()

        # Crear la solicitud de aprobación
        # Importar ApprovalRequestCreate localmente o usar el módulo completo si es necesario
        from app.auditing.schemas import ApprovalRequestCreate
        
        approval_request_in = ApprovalRequestCreate(
            entity_type="ASSET",
            entity_id=asset_id,
            action="DELETE_ASSET",
            request_justification=justification,
            payload={} 
        )
        approval_request = self.approval_service.create_request(approval_request_in, user, tenant_id)
        
        self.audit_service.log_operation(user, "REQUEST_DELETE_ASSET", db_asset)
        return approval_request

    def _execute_delete_asset(self, asset_id: uuid.UUID, tenant_id: uuid.UUID) -> models.Asset:
        """
        (Método interno) Ejecuta el borrado lógico del activo.
        Este método es llamado por el ApprovalService.
        """
        db_asset = self.asset_repo.get_asset(asset_id, tenant_id)
        if not db_asset:
            raise NotFoundException("Activo no encontrado durante la ejecución del borrado.")
        
        db_asset.status = "decommissioned"
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset
